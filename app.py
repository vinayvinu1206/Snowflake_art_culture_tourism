import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import snowflake.connector

# Set Streamlit page config
st.set_page_config(page_title="Art, Culture & Tourism", layout="wide")
st.title("Art, Culture and Tourism: Bridging Art, Culture & Tourism with Technology")

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"],
    client_session_keep_alive=True
)

def run_query(query):
    cur = conn.cursor()
    cur.execute(query)
    df = cur.fetch_pandas_all()
    cur.close()
    return df

# Load datasets from Snowflake
funds_df = run_query("SELECT * FROM RS_SESSION_250_AU186")
project_df = run_query("SELECT * FROM CONVERGENCEPROJECT_CONSERVATION")
tourism_df = run_query("SELECT * FROM TOURISM_STATISTICS_SINCE_1991_2")
iti_df = run_query('SELECT * FROM \"SES_2007-08_enrl_tech_indus\"')

# Rename columns
funds_df.columns = ['Year', 'Funds_Allocated_Cr', 'Funds_Utilized_Cr']
tourism_df.columns = ['Year', 'Foreign_Tourist_Numbers', 'Earnings_Cr', 'Earnings_USD', 'Domestic_Tourist_Numbers']
iti_df.columns = ['State_UT', 'ITI_Count', 'Intake_Capacity']

# Clean and convert year formats
funds_df['Year'] = funds_df['Year'].astype(str).str.extract(r'(\d{4})').astype(int)
tourism_df['Year'] = tourism_df['Year'].astype(int)

# Define your tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🧾 Culture Fund Utilization",
    "📈 Tourism Trends",
    "🏛️ Heritage Projects",
    "🎨 Art & Technical Training"
])

# Tab 1: Culture Fund Utilization
with tab1:
    st.subheader("Ministry of Culture: Funds Allocation vs Utilization (₹ Cr)")
    st.dataframe(funds_df, use_container_width=True)

    # Plotting with dual Y axes
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax2 = ax1.twinx()

    ax1.plot(funds_df['Year'], funds_df['Funds_Allocated_Cr'], color='blue', marker='o', label='Allocated')
    ax2.plot(funds_df['Year'], funds_df['Funds_Utilized_Cr'], color='orange', marker='o', label='Utilized')

    # Highlight max/min for Allocated
    max_alloc = funds_df['Funds_Allocated_Cr'].max()
    min_alloc = funds_df['Funds_Allocated_Cr'].min()
    max_year_alloc = funds_df.loc[funds_df['Funds_Allocated_Cr'].idxmax(), 'Year']
    min_year_alloc = funds_df.loc[funds_df['Funds_Allocated_Cr'].idxmin(), 'Year']
    ax1.scatter([max_year_alloc], [max_alloc], color='green', zorder=5)
    ax1.scatter([min_year_alloc], [min_alloc], color='red', zorder=5)
    ax1.text(max_year_alloc, max_alloc, f' ₹{max_alloc}', color='green', fontsize=9)
    ax1.text(min_year_alloc, min_alloc, f' ₹{min_alloc}', color='red', fontsize=9)

    # Highlight max/min for Utilized
    max_util = funds_df['Funds_Utilized_Cr'].max()
    max_year_util = funds_df.loc[funds_df['Funds_Utilized_Cr'].idxmax(), 'Year']
    min_year_util = funds_df.loc[funds_df['Funds_Utilized_Cr'].idxmin(), 'Year']
    ax2.scatter([max_year_util], [max_util], color='green', zorder=5)
    ax2.text(max_year_util, max_util, f' ₹{max_util}', color='green', fontsize=9)

    # Labels and formatting
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Funds Allocated (₹ Cr)", color='blue')
    ax2.set_ylabel("Funds Utilized (₹ Cr)", color='orange')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax2.tick_params(axis='y', labelcolor='orange')
    ax1.set_xticks(funds_df['Year'])

    # Title and grid
    plt.title("Funds Allocated vs Utilized - Dual Axis View")
    ax1.grid(True)

    st.pyplot(fig)

# Tab 2: Tourism Trends
import matplotlib.ticker as mticker

with tab2:
    st.subheader("Tourism Trends Over Years")

    # Ensure year is string
    tourism_df['Year'] = tourism_df['Year'].astype(str)

    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax2 = ax1.twinx()

    # Plot lines
    ax1.plot(tourism_df['Year'], tourism_df['Domestic_Tourist_Numbers'], label='Domestic Tourist Visits', color='skyblue', marker='o')
    ax2.plot(tourism_df['Year'], tourism_df['Foreign_Tourist_Numbers'], label='Foreign Tourist Arrivals', color='orange', marker='o')

    # Format Y axes (remove scientific notation)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    ax1.set_ylabel("Domestic Tourist Visits", color='skyblue')
    ax2.set_ylabel("Foreign Tourist Arrivals", color='orange')
    ax1.set_xlabel("Year")
    ax1.tick_params(axis='y', labelcolor='skyblue')
    ax2.tick_params(axis='y', labelcolor='orange')

    # Title and X-axis formatting
    plt.title("Tourism Trends Over Years")
    ax1.set_xticks(range(0, len(tourism_df['Year']), 2))
    ax1.set_xticklabels(tourism_df['Year'][::2], rotation=45)

    # Annotate Min/Max values
    min_domestic = tourism_df['Domestic_Tourist_Numbers'].min()
    max_domestic = tourism_df['Domestic_Tourist_Numbers'].max()
    year_min_dom = tourism_df.loc[tourism_df['Domestic_Tourist_Numbers'] == min_domestic, 'Year'].values[0]
    year_max_dom = tourism_df.loc[tourism_df['Domestic_Tourist_Numbers'] == max_domestic, 'Year'].values[0]
    ax1.annotate(f'Min: {min_domestic:,}', xy=(year_min_dom, min_domestic), xytext=(0, -30), textcoords='offset points', color='blue', arrowprops=dict(arrowstyle='->', color='blue'))
    ax1.annotate(f'Max: {max_domestic:,}', xy=(year_max_dom, max_domestic), xytext=(0, 10), textcoords='offset points', color='blue', arrowprops=dict(arrowstyle='->', color='blue'))

    min_foreign = tourism_df['Foreign_Tourist_Numbers'].min()
    max_foreign = tourism_df['Foreign_Tourist_Numbers'].max()
    year_min_for = tourism_df.loc[tourism_df['Foreign_Tourist_Numbers'] == min_foreign, 'Year'].values[0]
    year_max_for = tourism_df.loc[tourism_df['Foreign_Tourist_Numbers'] == max_foreign, 'Year'].values[0]
    ax2.annotate(f'Min: {min_foreign:,}', xy=(year_min_for, min_foreign), xytext=(0, -30), textcoords='offset points', color='darkorange', arrowprops=dict(arrowstyle='->', color='darkorange'))
    ax2.annotate(f'Max: {max_foreign:,}', xy=(year_max_for, max_foreign), xytext=(0, 10), textcoords='offset points', color='darkorange', arrowprops=dict(arrowstyle='->', color='darkorange'))

    # Show legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Show plot
    st.pyplot(fig)

    # Display min/max values below the chart
    st.markdown(f"**Domestic Tourist Visits:** Min = `{min_domestic:,}`, Max = `{max_domestic:,}`")
    st.markdown(f"**Foreign Tourist Arrivals:** Min = `{min_foreign:,}`, Max = `{max_foreign:,}`")



import pandas as pd
import streamlit as st

# Tab 3: Heritage Conservation – Mubarak Mandi Palace Complex
with tab3:
    st.subheader("Case Study: Conservation of Mubarak Mandi Palace Complex, Jammu")

    # Read data from the uploaded file
    project_df = pd.read_csv("Convergenceproject_Conservation.csv")

    # Rename columns for clarity
    project_df.rename(columns={
        'c1': 'Component',
        'c2': 'Description',
        'c3': 'Estimated Cost (₹ Cr)'
    }, inplace=True)

    # Display the project components
    st.markdown("### Project Components and Costs")
    st.dataframe(project_df, use_container_width=True)

    # Detailed Project Overview
    st.markdown("### 🏗️ Project Overview")
    st.markdown("""
    - **Location**: Jammu, Jammu & Kashmir, India  
    - **Heritage Site**: Mubarak Mandi Palace Complex  
    - **Scope**: Conservation of historic structures, development of public amenities, landscaping, and infrastructure enhancement.  
    - **Total Estimated Cost**: ₹486.62 Cr  
    - **Project Duration**: Initiated in March 2018; ongoing.  
    - **Client**: Mubarak Mandi Jammu Heritage Society  
    - **Consultants**: Architecture Heritage Division, INTACH  
    - **Area**: Approximately 15 acres  
    - **Status**: Ongoing conservation and revitalization efforts.  
    """)

    # Historical Significance
    st.markdown("### 🕰️ Historical Significance")
    st.markdown("""
    The Mubarak Mandi Palace Complex, dating back to the early 19th century, served as the royal residence of the Dogra dynasty. 
    The complex showcases a blend of Rajasthani, Mughal, and European architectural styles. Notable structures within the complex 
    include the Darbar Hall, Sheesh Mahal, Pink Palace, Royal Courts, and Rani Charak Palace. Over the years, the complex has 
    witnessed significant historical events and has been a symbol of Jammu's rich cultural heritage.
    """)

    # Conservation Efforts
    st.markdown("### 🛠️ Conservation Efforts")
    st.markdown("""
    The conservation project encompasses:  
    - **Structural Restoration**: Stabilizing and restoring deteriorated structures within the complex.  
    - **Infrastructure Development**: Enhancing accessibility through the introduction of battery-operated vehicles, signage, and parking facilities.  
    - **Landscape Revitalization**: Developing gardens and open spaces to enhance the aesthetic appeal.  
    - **Adaptive Reuse**: Transforming parts of the complex into museums, cultural centers, and conference facilities to promote tourism and cultural activities.  
    - **Connectivity Enhancement**: Plans to connect the complex with nearby heritage sites like Bahu Fort via a proposed ropeway.  
    """)

    # Challenges and Mitigation
    st.markdown("### ⚠️ Challenges and Mitigation")
    st.markdown("""
    - **Structural Degradation**: The complex has suffered from multiple fires (over 36 incidents) and earthquakes, leading to significant damage.  
    - **Neglect and Encroachment**: Years of neglect have resulted in encroachments and unauthorized modifications.  
    - **Resource Constraints**: Limited funding and skilled manpower pose challenges to timely restoration.  
    - **Mitigation Measures**: The government has initiated phased conservation plans, with 33 projects in Phase I and 73 more identified in Phase II, ensuring structured and well-funded restoration efforts.  
    """)

    # Conclusion
    st.markdown("### ✅ Conclusion")
    st.markdown("""
    The conservation of the Mubarak Mandi Palace Complex is a testament to the commitment towards preserving Jammu's rich 
    cultural and architectural heritage. Through meticulous planning and execution, the project aims to restore the complex 
    to its former glory, making it a hub for cultural tourism and community engagement.
    """)



# Tab 4: ITI/ITC Data
with tab4:
    st.subheader("🎨 State-wise ITI/ITC Distribution")

    # Sort for main table
    sorted_iti_df = iti_df.sort_values(by='Intake_Capacity', ascending=False)

    # Show DataFrame
    st.dataframe(sorted_iti_df, use_container_width=True)

    # Key metrics
    total_itis = iti_df['ITI_Count'].sum()
    total_capacity = iti_df['Intake_Capacity'].sum()
    avg_capacity_per_iti = round(total_capacity / total_itis, 2)

    top_state_capacity = iti_df.loc[iti_df['Intake_Capacity'].idxmax()]
    top_state_count = iti_df.loc[iti_df['ITI_Count'].idxmax()]

    st.markdown(f"""
    #### 📊 Key Insights:
    - 🏅 **Top State by Intake Capacity**: `{top_state_capacity['State_UT']}` with **{top_state_capacity['Intake_Capacity']:,}` seats
    - 🏅 **Top State by Number of ITIs**: `{top_state_count['State_UT']}` with **{top_state_count['ITI_Count']:,}` institutes
    - 📈 **Total ITIs**: `{total_itis:,}`
    - 👥 **Total Intake Capacity**: `{total_capacity:,}`
    - ⚖️ **Average Capacity per ITI**: `{avg_capacity_per_iti}`
    """)

    # Chart 1: Top 10 states by Intake Capacity
    st.markdown("### 🔟 Top 10 States by Intake Capacity")
    top_capacity_states = sorted_iti_df.head(10)
    fig1, ax1 = plt.subplots()
    sns.barplot(x='Intake_Capacity', y='State_UT', data=top_capacity_states, ax=ax1, palette='Blues_r')
    ax1.set_xlabel("Intake Capacity")
    ax1.set_ylabel("State/UT")
    st.pyplot(fig1)

    # Chart 2: Top 10 states by ITI Count
    st.markdown("### 🏫 Top 10 States by Number of ITIs")
    top_iti_count = iti_df.sort_values(by='ITI_Count', ascending=False).head(10)
    fig2, ax2 = plt.subplots()
    sns.barplot(x='ITI_Count', y='State_UT', data=top_iti_count, ax=ax2, palette='Greens_r')
    ax2.set_xlabel("Number of ITIs")
    ax2.set_ylabel("State/UT")
    st.pyplot(fig2)

    # Chart 3: Scatter plot - ITI Count vs Intake Capacity
    st.markdown("### 🔍 Correlation between ITI Count and Intake Capacity")
    fig3, ax3 = plt.subplots()
    sns.scatterplot(x='ITI_Count', y='Intake_Capacity', hue='State_UT', data=iti_df, s=100, palette='tab10', ax=ax3)
    ax3.set_xlabel("Number of ITIs")
    ax3.set_ylabel("Intake Capacity")
    ax3.set_title("ITI Count vs Intake Capacity by State")
    st.pyplot(fig3)

