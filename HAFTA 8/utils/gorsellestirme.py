import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def transparan_layout_uygula(fig):
    """
    Plotly grafiklerine fütüristik şeffaf tasarımı (Glassmorphism uyumlu) uygular.
    """
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(t=40) # l, r, b silindi. Plotly artık yazıları sıkıştırmadan otomatik yer açacak!
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig

def ciz_en_cok_satanlar(df):
    en_cok_satilanlar = df['product_name'].value_counts().head(10).reset_index()
    en_cok_satilanlar.columns = ['Ürün', 'Adet']
    en_cok_satilanlar = en_cok_satilanlar.sort_values(by='Adet', ascending=True)
    
    fig = px.bar(
        en_cok_satilanlar, x='Adet', y='Ürün', orientation='h',
        color='Adet', color_continuous_scale='Purp',
        title="En Çok Satan 10 Ürün (Adet Bazlı)"
    )
    
    # Y eksenindeki 'Ürün' yazısını kaldır ve uzun isimlerin kesilmemesi için automargin ekle
    fig.update_yaxes(title="", automargin=True)
    
    return transparan_layout_uygula(fig)

def ciz_gercek_sadakat(df):
    urun_satis = df['product_name'].value_counts()
    populer = urun_satis[urun_satis > 100].index
    
    if len(populer) == 0:
        return px.bar(title="Yeterli Veri Yok")
        
    sadakat = df[df['product_name'].isin(populer)].groupby('product_name')['reordered'].mean() * 100
    sadakat_df = sadakat.sort_values(ascending=False).head(10).reset_index()
    sadakat_df.columns = ['Ürün', 'Sadakat Oranı (%)']
    sadakat_df = sadakat_df.sort_values(by='Sadakat Oranı (%)', ascending=True)
    
    fig = px.bar(
        sadakat_df, x='Sadakat Oranı (%)', y='Ürün', orientation='h',
        color='Sadakat Oranı (%)', color_continuous_scale='Teal',
        title="Gerçek Sadakat (Oran Bazlı)"
    )
    
    # Y eksenindeki 'Ürün' yazısını kaldır ve uzun isimlerin kesilmemesi için automargin ekle
    fig.update_yaxes(title="", automargin=True)
    
    return transparan_layout_uygula(fig)

def ciz_sepet_buyuklugu(df):
    sepetler = df.groupby('order_id').size().reset_index(name='Ürün Sayısı')
    sepetler = sepetler[sepetler['Ürün Sayısı'] <= 50] # Aykırı değerleri kes
    
    fig = px.histogram(
        sepetler, x='Ürün Sayısı', nbins=50,
        color_discrete_sequence=['#06b6d4'],
        title="Sepet Büyüklüğü Dağılımı"
    )
    
    # Y eksenindeki otomatik İngilizce 'count' yazısını Türkçeye ('Sepet Adedi') çevir ve sığdır.
    fig.update_yaxes(title="Sepet Adedi", automargin=True)
    
    return transparan_layout_uygula(fig)

def ciz_heatmap(df):
    # order_dow (0=Cmt, 1=Paz) ve order_hour_of_day'e göre grupla
    heatmap_data = df.groupby(['order_dow', 'order_hour_of_day']).size().reset_index(name='Sipariş Sayısı')
    heatmap_pivot = heatmap_data.pivot(index='order_dow', columns='order_hour_of_day', values='Sipariş Sayısı').fillna(0)
    
    gunler = ['Cumartesi', 'Pazar', 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']
    heatmap_pivot.index = gunler[:len(heatmap_pivot.index)]
    
    fig = px.imshow(
        heatmap_pivot, 
        labels=dict(x="Günün Saati", y="Haftanın Günü", color="Sipariş"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        color_continuous_scale='Plasma',
        title="Sipariş Yoğunluğu Isı Haritası (Prime-Time)"
    )
    return transparan_layout_uygula(fig)

def ciz_network_graph(kurallar_df):
    """
    Birliktelik kurallarını görselleştirmek için Plotly ile Scatter (Network) grafiği çizer.
    """
    if kurallar_df.empty:
        return go.Figure().update_layout(title="Kural Bulunamadı", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        
    # En güçlü ilk 15 kuralı al
    top_kurallar = kurallar_df.sort_values('lift', ascending=False).head(15)
    
    # Node (düğüm) koordinatları oluştur (Basit çember dizilimi)
    nodes = list(set(top_kurallar['antecedents']).union(set(top_kurallar['consequents'])))
    import numpy as np
    
    node_x = []
    node_y = []
    for i in range(len(nodes)):
        angle = 2 * np.pi * i / len(nodes)
        node_x.append(np.cos(angle))
        node_y.append(np.sin(angle))
        
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=nodes, textposition="bottom center",
        hoverinfo='text',
        marker=dict(size=20, color='#8b5cf6', line=dict(width=2, color='white'))
    )
    
    edge_x = []
    edge_y = []
    for _, row in top_kurallar.iterrows():
        x0 = node_x[nodes.index(row['antecedents'])]
        y0 = node_y[nodes.index(row['antecedents'])]
        x1 = node_x[nodes.index(row['consequents'])]
        y1 = node_y[nodes.index(row['consequents'])]
        
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#06b6d4'),
        hoverinfo='none',
        mode='lines'
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title='Ürün Birliktelik Ağı (Network Graph)',
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig
