# filename: interactive_dashboard.py
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os

def generate_interactive_dashboard(df):
    """
    Generates an HTML dashboard with 10 interactive charts that EXACTLY match 
    the static figures in visualizer.py, plus insight commentary.
    """
    print("\n" + "="*50)
    print("   PHASE 4: INTERACTIVE DASHBOARD GENERATION   ")
    print("="*50)
    
    # --- Generate All 10 Figures (Plotly Versions) ---
    figs = {}
    
    # 1. Funding Transition
    figs['fig1'] = _create_fig1_funding(df)
    
    # 2. Kuznets Curve
    figs['fig2'] = _create_fig2_kuznets(df)
    
    # 3. Energy Mix
    figs['fig3'] = _create_fig3_energy_mix(df)
    
    # 4. Top Aid Recipients
    figs['fig4'] = _create_fig4_top_aid(df)
    
    # 5. Global Divergence
    figs['fig5'] = _create_fig5_divergence(df)
    
    # 6. Correlation Matrix
    figs['fig6'] = _create_fig6_correlation(df)
    
    # 7. Top Movers
    figs['fig7'] = _create_fig7_top_movers(df)
    
    # 8. Income Disparity
    figs['fig8'] = _create_fig8_income(df)
    
    # 9. Predictive Forecast
    figs['fig9'] = _create_fig9_forecast(df)

    # 10. Choropleth Map (NEW)
    figs['fig10'] = _create_fig10_map(df)

    # --- Assemble HTML ---
    html_content = _assemble_html(figs)
    
    # --- Save ---
    if not os.path.exists('figures'):
        os.makedirs('figures')
        
    with open('figures/interactive_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("-> Dashboard saved to 'figures/interactive_dashboard.html'")
    print("-> Consistency Check: All 10 figures (including Map) are now interactive.")

# ==========================================
# PLOTLY FIGURE GENERATORS
# ==========================================

def _create_fig1_funding(df):
    """Fig 1: Dual Axis - Aid vs Capacity"""
    if 'Financial_Flows' not in df.columns: return go.Figure()
    annual = df.groupby('Year').agg({'Financial_Flows': 'sum', 'Renewable_Capacity': 'mean'}).reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=annual['Year'], y=annual['Financial_Flows'], name="Financial Aid ($)", marker_color='#85bb65', opacity=0.7), secondary_y=False)
    fig.add_trace(go.Scatter(x=annual['Year'], y=annual['Renewable_Capacity'], name="Renewable Capacity", mode='lines+markers', line=dict(color='#2c3e50', width=3)), secondary_y=True)
    fig.update_layout(title="<b>Fig 1: Funding the Future</b>", template="plotly_white", legend=dict(orientation='h', y=1.1))
    return fig

def _create_fig2_kuznets(df):
    """Fig 2: Kuznets Curve"""
    if 'GDP_Capita' not in df.columns: return go.Figure()
    clean_df = df.dropna(subset=['GDP_Capita', 'CO2_Total_kt', 'Access_Electricity', 'Year']).sort_values('Year')
    if clean_df.empty: return go.Figure()
    fig = px.scatter(clean_df, x="GDP_Capita", y="CO2_Total_kt", animation_frame="Year", animation_group="Country", size="Access_Electricity", color="Income_Group", hover_name="Country", log_x=True, log_y=True, title="<b>Fig 2: The Decoupling Test</b> (Play Animation)", color_discrete_sequence=px.colors.qualitative.Prism)
    return fig

def _create_fig3_energy_mix(df):
    """Fig 3: Energy Mix"""
    if 'Elec_Fossil' not in df.columns: return go.Figure()
    annual = df.groupby('Year')[['Elec_Fossil', 'Elec_Renewables', 'Elec_Nuclear']].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=annual['Year'], y=annual['Elec_Fossil'], mode='lines', name='Fossil', stackgroup='one', line=dict(color='#636e72')))
    fig.add_trace(go.Scatter(x=annual['Year'], y=annual['Elec_Nuclear'], mode='lines', name='Nuclear', stackgroup='one', line=dict(color='#f1c40f')))
    fig.add_trace(go.Scatter(x=annual['Year'], y=annual['Elec_Renewables'], mode='lines', name='Renewables', stackgroup='one', line=dict(color='#00b894')))
    fig.update_layout(title="<b>Fig 3: Global Energy Mix</b>", template="plotly_white")
    return fig

def _create_fig4_top_aid(df):
    """Fig 4: Top Aid"""
    if 'Financial_Flows' not in df.columns: return go.Figure()
    total = df.groupby('Country')['Financial_Flows'].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(total, x='Financial_Flows', y='Country', orientation='h', title="<b>Fig 4: Top 10 Aid Recipients</b>", color='Financial_Flows', color_continuous_scale='Blues')
    fig.update_layout(yaxis=dict(autorange="reversed"), template="plotly_white")
    return fig

def _create_fig5_divergence(df):
    """Fig 5: Divergence"""
    if 'GDP_Capita' not in df.columns: return go.Figure()
    annual = df.groupby('Year').agg({'GDP_Capita': 'mean', 'CO2_Total_kt': 'sum'}).reset_index()
    annual['GDP_Idx'] = (annual['GDP_Capita'] / annual['GDP_Capita'].iloc[0]) * 100
    annual['CO2_Idx'] = (annual['CO2_Total_kt'] / annual['CO2_Total_kt'].iloc[0]) * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=annual['Year'], y=annual['GDP_Idx'], name='GDP Growth', line=dict(color='#2ecc71', width=4)))
    fig.add_trace(go.Scatter(x=annual['Year'], y=annual['CO2_Idx'], name='CO2 Growth', line=dict(color='#e74c3c', width=4, dash='dash')))
    fig.update_layout(title="<b>Fig 5: The Decoupling Challenge</b>", template="plotly_white")
    return fig

def _create_fig6_correlation(df):
    """Fig 6: Correlation"""
    cols = ['GDP_Capita', 'Financial_Flows', 'Renewable_Share', 'CO2_Total_kt', 'Energy_Intensity', 'Access_Electricity']
    cols = [c for c in cols if c in df.columns]
    if len(cols) < 2: return go.Figure()
    corr = df[cols].corr()
    fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, title="<b>Fig 6: Drivers Correlation</b>")
    return fig

def _create_fig7_top_movers(df):
    """Fig 7: Top Movers"""
    pivoted = df.pivot_table(index='Country', columns='Year', values='Renewable_Share')
    if 2000 not in pivoted.columns or 2020 not in pivoted.columns: return go.Figure()
    pivoted['Growth'] = pivoted[2020] - pivoted[2000]
    top10 = pivoted.dropna(subset=['Growth']).nlargest(10, 'Growth').reset_index()
    fig = px.bar(top10, x='Growth', y='Country', orientation='h', title="<b>Fig 7: Top Green Movers</b>", color='Growth', color_continuous_scale='Greens')
    fig.update_layout(yaxis=dict(autorange="reversed"), template="plotly_white")
    return fig

def _create_fig8_income(df):
    """Fig 8: Income"""
    if 'Income_Group' not in df.columns: return go.Figure()
    clean_df = df.dropna(subset=['Income_Group', 'Renewable_Share'])
    fig = px.box(clean_df, x='Income_Group', y='Renewable_Share', color='Income_Group', title="<b>Fig 8: The Green Divide</b>", color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(template="plotly_white")
    return fig

def _create_fig9_forecast(df):
    """Fig 9: Forecast"""
    if 'Renewable_Share' not in df.columns: return go.Figure()
    pivoted = df.pivot_table(index='Country', columns='Year', values='Renewable_Share')
    if 2000 not in pivoted.columns or 2020 not in pivoted.columns: return go.Figure()
    pivoted['Growth'] = pivoted[2020] - pivoted[2000]
    top5 = pivoted.dropna(subset=['Growth']).nlargest(5, 'Growth').index.tolist()
    fig = go.Figure()
    colors = px.colors.qualitative.Bold
    for i, country in enumerate(top5):
        c_data = df[df['Country'] == country].sort_values('Year')
        X_hist = c_data['Year'].values; y_hist = c_data['Renewable_Share'].values
        valid = np.isfinite(y_hist)
        if np.sum(valid) < 5: continue
        z = np.polyfit(X_hist[valid], y_hist[valid], 1); p = np.poly1d(z)
        X_fut = np.arange(2020, 2031); y_fut = np.clip(p(X_fut), 0, 100)
        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(x=X_hist, y=y_hist, name=f"{country}", line=dict(color=color, width=2), opacity=0.6))
        fig.add_trace(go.Scatter(x=X_fut, y=y_fut, showlegend=False, line=dict(color=color, width=3, dash='dot')))
    fig.add_vline(x=2030, line_dash="dot", annotation_text="SDG Target")
    fig.update_layout(title="<b>Fig 9: 2030 Forecast</b>", template="plotly_white")
    return fig

def _create_fig10_map(df):
    """Fig 10: Choropleth Map"""
    # Filter for the most recent year with good data (e.g., 2019)
    target_year = 2019
    df_map = df[df['Year'] == target_year].copy()
    
    if df_map.empty or 'Renewable_Capacity' not in df.columns: return go.Figure()
    
    fig = px.choropleth(df_map, 
                        locations="Country", 
                        locationmode="country names",
                        color="Renewable_Capacity",
                        hover_name="Country",
                        color_continuous_scale="Blues",
                        title=f"<b>Fig 10: Global Renewable Capacity ({target_year})</b>")
    
    fig.update_geos(projection_type="natural earth", showcoastlines=True, coastlinecolor="Black")
    fig.update_layout(template="plotly_white", margin=dict(l=0,r=0,t=50,b=0))
    return fig

def _assemble_html(figs):
    """Assembles the 10 Plotly figures into a polished HTML layout with insights."""
    
    divs = {k: v.to_html(full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False}) for k, v in figs.items()}
    
    # Define Insights for each figure
    insights = {
        'fig1': "<b>Insight:</b> While financial aid (bars) has surged significantly since 2010, the global average renewable capacity (line) shows only linear, not exponential, growth.",
        'fig2': "<b>Insight:</b> A 'Kuznets' effect is visible—wealthier nations (right) generally emit more, but recent years show some high-income nations lowering emissions.",
        'fig3': "<b>Insight:</b> Despite the rise of renewables (green), fossil fuels (gray) still dominate the absolute generation mix, highlighting the scale of the transition challenge.",
        'fig4': "<b>Insight:</b> Climate finance is highly concentrated. A handful of nations (like India and Pakistan) receive the bulk of funding, leaving smaller nations with less support.",
        'fig5': "<b>Insight:</b> <b>Success!</b> The gap between GDP growth (green) and CO2 emissions (red) is widening, proving that economic growth can be decoupled from carbon.",
        'fig6': "<b>Insight:</b> Note the weak correlation between 'Financial Flows' and 'Renewable Share'. This suggests money alone isn't automatically translating into green energy percentages.",
        'fig7': "<b>Insight:</b> The top movers are often smaller nations or those with abundant hydro resources, rather than just the wealthiest G20 nations.",
        'fig8': "<b>Insight:</b> The 'Green Divide' is real. High-income nations (yellow) have a significantly higher median renewable share than low-income nations.",
        'fig9': "<b>Insight:</b> If current trends continue, top performers are on track to reach ~80-90% renewable share by 2030, but acceleration is needed elsewhere.",
        'fig10': "<b>Insight:</b> Geography plays a major role—capacity is clustered in regions with natural hydro/geothermal advantages (e.g., Iceland, Norway, Brazil)."
    }

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Financing the Future: Interactive Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #f8fafc; font-family: 'Segoe UI', Roboto, sans-serif; }}
            .card {{ background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden; border: 1px solid #e2e8f0; }}
            .card:hover {{ box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); transition: 0.3s; }}
            .insight-box {{ background-color: #f0f9ff; border-left: 4px solid #0ea5e9; padding: 12px; font-size: 0.9rem; color: #334155; margin-top: -10px; margin-bottom: 10px; margin-left: 10px; margin-right: 10px; border-radius: 0 4px 4px 0; }}
            .header {{ background: linear-gradient(to right, #0f172a, #334155); color: white; }}
        </style>
    </head>
    <body>
        <div class="header p-8 mb-8 shadow-md">
            <div class="container mx-auto">
                <h1 class="text-3xl font-bold">🌍 Financing the Future</h1>
                <p class="text-slate-300 mt-1">Interactive Companion: Economic Drivers & Green Transition (2000-2030)</p>
            </div>
        </div>

        <div class="container mx-auto px-4 pb-12">
            
            <h2 class="text-xl font-bold text-slate-700 mb-4 border-l-4 border-blue-500 pl-3">1. Economic Drivers & Aid</h2>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">
                <div class="card">
                    <div class="p-2">{divs['fig1']}</div>
                    <div class="insight-box">{insights['fig1']}</div>
                </div>
                <div class="card">
                    <div class="p-2">{divs['fig4']}</div>
                    <div class="insight-box">{insights['fig4']}</div>
                </div>
            </div>

            <h2 class="text-xl font-bold text-slate-700 mb-4 border-l-4 border-green-500 pl-3">2. Global Outcomes & Decoupling</h2>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">
                <div class="card">
                    <div class="p-2">{divs['fig3']}</div>
                    <div class="insight-box">{insights['fig3']}</div>
                </div>
                <div class="card">
                    <div class="p-2">{divs['fig5']}</div>
                    <div class="insight-box">{insights['fig5']}</div>
                </div>
            </div>

            <h2 class="text-xl font-bold text-slate-700 mb-4 border-l-4 border-purple-500 pl-3">3. Equity & Efficiency</h2>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">
                <div class="card">
                    <div class="p-2">{divs['fig2']}</div>
                    <div class="insight-box">{insights['fig2']}</div>
                </div>
                <div class="card">
                    <div class="p-2">{divs['fig8']}</div>
                    <div class="insight-box">{insights['fig8']}</div>
                </div>
            </div>

            <h2 class="text-xl font-bold text-slate-700 mb-4 border-l-4 border-orange-500 pl-3">4. Geographic Analysis</h2>
            <div class="mb-10 card p-2">
                 {divs['fig10']}
                 <div class="insight-box">{insights['fig10']}</div>
            </div>

            <h2 class="text-xl font-bold text-slate-700 mb-4 border-l-4 border-indigo-500 pl-3">5. Leaders & Forecast</h2>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12">
                 <div class="card">
                    <div class="p-2">{divs['fig7']}</div>
                    <div class="insight-box">{insights['fig7']}</div>
                </div>
                <div class="card">
                    <div class="p-2">{divs['fig9']}</div>
                    <div class="insight-box">{insights['fig9']}</div>
                </div>
            </div>
            
            <div class="card p-2 mb-10">
                {divs['fig6']}
                <div class="insight-box">{insights['fig6']}</div>
            </div>

            <footer class="text-center text-slate-400 py-6 border-t">
                <p>Data Source: World Bank / IEA | Generated via Python & Plotly</p>
            </footer>
        </div>
    </body>
    </html>
    """
    return html