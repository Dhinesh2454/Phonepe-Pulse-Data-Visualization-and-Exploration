import streamlit as st
import mysql.connector 
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import requests
import json
import geopandas as gpd
#==========================================MYSQL Database Connection====================================#
#database connection parameters
mydb=mysql.connector.connect(host="127.0.0.1",
                            user="root",
                            password="Dhinesh@2454",
                            database="phonepayplus",
                            auth_plugin="mysql_native_password")

cursor=mydb.cursor()

# Aggregated Transation dataframe
cursor.execute("SELECT * FROM aggregated_trans;")
#fetch the data from mysql database
Agg_trans=cursor.fetchall()
Agg_trans_df=pd.DataFrame(Agg_trans,columns=("State","Year","Quarter","Transation_type","Transation_count","Transation_amount"))

# Aggregated user Dataframe
cursor.execute("SELECT * FROM aggregated_user")
#fetch the data from mysql database
Agg_user=cursor.fetchall()
Agg_user_df=pd.DataFrame(Agg_user,columns=("State","Year","Quarter","Brand_name","User_count","Percentage"))

# Map Transation Dataframe
cursor.execute("SELECT * FROM map_transation;")
#fetch the data from mysql database
Map_trans=cursor.fetchall()
Map_trans_df=pd.DataFrame(Map_trans,columns=("State","Year","Quarter","District_name","Transation_count","Transation_amount"))

#Map user dataframe
cursor.execute("SELECT * FROM map_user;")
#fetch the data from mysql database
Map_user=cursor.fetchall()
Map_user_df=pd.DataFrame(Map_user,columns=("State","Year","Quarter","District_name","Registeredusers_count","AppOpen_count"))


# Top Transation Dataframe
cursor.execute("SELECT * FROM top_trans;")
#fetch the data from mysql database
Top_trans=cursor.fetchall()
Top_trans_df=pd.DataFrame(Top_trans,columns=("State","Year","Quarter","Pincode","District_name","Transation_count","Transation_amount"))

# Top User Dataframe
cursor.execute("SELECT * FROM top_user;")
#fetch the data from mysql database
Top_user=cursor.fetchall()
Top_user_df=pd.DataFrame(Top_user,columns=("State","Year","Quarter","Pincode","District_name","User_count"))

# function to formates a number with currency symbol and comma separation. 
def format_number(number):
    return '₹'+"{:,.0f}".format(number)
# function to formates a numbers into crores with currency symbol
def mcrores(number):
    return '₹'+'{:,.0f} Cr'.format(round(number / 10000000))
# function to formate a numbers with comma separation
def format_number1(number):
        number_str = "{:,.0f}".format(number)
        return number_str.replace(",", ",")
#================================ Home Page for streamlit dashboard===============================================#
st.set_page_config(layout="wide")
# Project Title
st.title(":rainbow[Phonepe Pulse Data Visualization and Exploration]")
#create streamlit tab 
tab1,tab2,tab3=st.tabs(["Home","State Wise Data Expolaration","Insights"])
# Home page setting
with tab1:
    c1,c2,c3=st.columns([1,1,1])
    # create selectbox for years
    with c1:
        y=["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
        default_y = y.index("2024")
        year = st.selectbox('Year',
                y,key='Year',index=default_y)
        if year=="2018":
            year=2018
        if year=="2019":
            year=2019
        if year=="2020":
            year=2020
        if year=="2021":
            year=2021
        if year=="2022":
            year=2022
        if year=="2023":
            year=2023
        if year=="2024":
            year=2024 
    # create selectbox for Quarters     
    with c2:
        q=["Q1","Q2","Q3","Q4"]

        default_q=q.index("Q1")
        Quarter=st.selectbox("Quarter"
                            ,q,key="Quarter",index=default_q)       
        if Quarter=="Q1":
            Quarter=1
            Qua="Q1"
        if Quarter=="Q2":
            Quarter=2
            if year==2024:
                st.warning("Data is not Available in Quarter = 2")
                Qua="Q2" 
        if Quarter=="Q3":
            Quarter=3
            if year==2024:
                st.warning("Data is not Available in Quarter = 3")
                Qua="Q3"
        if Quarter=="Q4":
            Quarter=4 
            if year==2024:
                st.warning("Data is not Available in Quarter = 4")
                Qua="Q4"
    # Create selectbox for Explore Data Options
    with c3:
        option=["Transation","User",]
        default_option=option.index("Transation")
        user_tran=st.selectbox(" ALL India",option,index=default_option)
        if user_tran=="Transation":
            df=Agg_trans_df
        
        if user_tran=="User":
            user_df=Map_user_df
    # ===============================Aggregated Transaction data Analysis==================================
    try:
        # filter the data based on specified year and quarter
        Agg_tran_filter=df[(df["Year"]==year) & (df["Quarter"]==Quarter)]
        # Reset index to ensure strats from 0 after filter
        Agg_tran_filter.reset_index(drop=True,inplace=True)
        # Groupby the transaction type and to calculate the sum of the Transactiom count and amount
        Agg_payment_type=Agg_tran_filter.groupby("Transation_type")[["Transation_count","Transation_amount"]].sum()
        #convert the aggregated data into dataframe                                                                                                                 
        payment_type_df=pd.DataFrame(Agg_payment_type)
        payment_type_df.reset_index(drop=False,inplace=True)
        #calculate the transation count and to formate the result
        tot_tran=payment_type_df["Transation_count"].sum()
        tot_tran_count=format_number1(tot_tran)
        #calculate the transation amount  and to formate the result
        tot_tran_va=payment_type_df["Transation_amount"].sum()

        tot_tran_value=mcrores(tot_tran_va)
        tot_tran_Av=round(tot_tran_va/tot_tran)
        tot_tran_Avar=format_number(tot_tran_Av)
        # display the results in dashboard
        tc1,tc2=st.columns([2.3,1])
        with tc2:
            st.header(":blue[Transation]")
            st.markdown("All PhonePe transactions (UPI + Cards + Wallets)")
            st.header(f":green[{tot_tran_count}]")
            tc3,tc4=st.columns(2)
            with tc3:
                st.markdown("Total Payment Value")
                
                st.markdown(f":green[{tot_tran_value}]")
            with tc4:
                st.markdown("Avg. transaction value")
                st.markdown(f":green[{tot_tran_Avar}]")
            st.header(":blue[Categories]")
            merc=payment_type_df["Transation_count"][1]
            peer=payment_type_df["Transation_count"][3]
            rech=payment_type_df["Transation_count"][4]
            fina=payment_type_df["Transation_count"][0]
            other=payment_type_df["Transation_count"][2]
            st.subheader("Merchant payments "" "f":green[{format_number1(merc)}]")
            st.subheader(f"Peer-to-peer payments" " " f":green[{format_number1(peer)}]")
            st.subheader("Recharge & bill payments" " " f":green[{format_number1(rech)}]")   
            st.subheader(f"Financial Services""  "f":green[{format_number1(fina)}]")    
            st.subheader("Others" " "f":green[{format_number1(other)}]") 
            fig_pie=px.pie(payment_type_df,values="Transation_count",hover_name="Transation_type",names="Transation_type",title=f"Categories Wise Split{year,Qua}")
            st.plotly_chart(fig_pie)
        # Map Transaction data proccing and map Visualization
        with tc1:
            # filter the data based on specified year and quarter
            map_filter=Map_trans_df[(Map_trans_df["Year"]==year) & (Map_trans_df["Quarter"]==Quarter)]
            map_filter.reset_index(drop=True,inplace=True)
            map_tran_group=map_filter.groupby("State")[["Transation_count","Transation_amount"]].sum()
            map_tran_df=pd.DataFrame(map_tran_group)
            map_tran_df.reset_index(inplace=True)
            # load the GeoJSON data for indian states 
            url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            respone=requests.get(url)
            india_states=json.loads(respone.content)
            #Extract state from the GeoJSON Data
            state_name=[]
            for features in india_states["features"]:
                state_name.append(features["properties"]["ST_NM"])
            state_name.sort()
            # create choropleth map for transaction Amount
            fig_map_amount =px.choropleth(map_tran_df,locations="State",geojson=india_states,featureidkey="properties.ST_NM",               
                                color="Transation_amount",
                                color_continuous_scale="Sunsetdark",
                                fitbounds="locations",
                                hover_name="State",title=f"PhonePe Amounts Transactions in {year,Qua} ",
                                width=1000,height=500)
            fig_map_amount .update_geos(visible=False )
            st.plotly_chart(fig_map_amount )
            # create choropleth map for transaction count
            fig_map_count  =px.choropleth(map_tran_df,locations="State",geojson=india_states,featureidkey="properties.ST_NM",
                                color="Transation_count",
                                color_continuous_scale="thermal",
                                fitbounds="locations",
                                hover_name="State",title=f"PhonePe Transactions count in {year,Qua} ",
                                width=1000,height=500)
            fig_map_count.update_geos(visible=False )
            st.plotly_chart(fig_map_count)
        # Groupby the State and to calculate the sum of the Transactiom count and amount
        Agtqg=Agg_tran_filter.groupby("State")[["Transation_amount","Transation_count"]].sum()
        Agtqg.reset_index(inplace=True)
        # Create bar chart for total transaction amount
        fig_amount=px.bar(Agtqg,x="State",y="Transation_amount",color="Transation_amount",height=500,width=1100,title=f"Total Transation Amount{year,Qua}")
        # Create bar chart for total transaction amount
        fig_count=px.bar(Agtqg,x="State",y="Transation_count",color="Transation_count",height=500,width=700,title=f"Total Transation count{year,Qua}")
        # Display the bar chart in streamlit columns
        d1,d2=st.columns([0.1,0.1])
        with d1:
            st.plotly_chart(fig_amount)
        with d2:
            st.plotly_chart(fig_count)
    except:
        pass
     #============================== Aggregated User data Analysis=======================================
    try:  
        # filter the data based on specified year and quarter
        Agg_user_filter=user_df[(user_df["Year"]==year) & (user_df["Quarter"]==Quarter)]
        Agg_user_filter.reset_index(drop=True,inplace=True)
        # Groupby the State and to calculate the sum of the Transactiom count and amount
        user_count_grp=Agg_user_filter.groupby(["State"])[["Registeredusers_count","AppOpen_count"]].sum()
        user_count_grp.reset_index(inplace=True)
        # Convert  Aggregated data into dataframe
        user_detail_df=pd.DataFrame(user_count_grp)
        Register=user_detail_df["Registeredusers_count"].sum()
        Register_user=format_number1(Register)
        Appopp=user_detail_df["AppOpen_count"].sum()
        Appopp_user=format_number1(Appopp)
        # display the results in dashboard
        tc1,tc2=st.columns([2.5,1])      
        with tc2:
            st.subheader(":blue[User]")
            st.markdown("Registered PhonePe users till "f"{Qua},{year} ")
            st.header(f":green[{Register_user}]")
            st.markdown("PhonePe app opens in "f"{Qua},{year} ")
            st.header(f":green[{Appopp_user}]")
        with tc1:
            # load the GeoJSON data for indian states 
            url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            respone=requests.get(url)
            india_states=json.loads(respone.content)
            #Extract state from the GeoJSON Data
            state_name=[]
            for features in india_states["features"]:
                state_name.append(features["properties"]["ST_NM"])
            state_name.sort()
            # create choropleth map for PhonePe Registeredusers count
            map_user_count =px.choropleth(user_detail_df,locations="State",geojson=india_states,featureidkey="properties.ST_NM",
                                color="Registeredusers_count",
                                color_continuous_scale="Sunsetdark",
                                fitbounds="locations",
                                hover_name="State",title=f"PhonePe Registeredusers count in {year,Qua} ",
                                width=1000,height=500)
            map_user_count .update_geos(visible=False )
            st.plotly_chart(map_user_count )
            # create choropleth map for PhonePe AppOpen count
            user_app_count  =px.choropleth(user_detail_df,locations="State",geojson=india_states,featureidkey="properties.ST_NM",
                                color="AppOpen_count",
                                color_continuous_scale="thermal",
                                fitbounds="locations",
                                hover_name="State",title=f"PhonePe AppOpen count in {year,Qua} ",
                                width=1000,height=500)
            user_app_count.update_geos(visible=False )
            st.plotly_chart(user_app_count)
            # Create Bar chart for PhonePe Registeredusers count 
            fig_regi_count=px.bar(user_count_grp,x="State",y="Registeredusers_count",color="Registeredusers_count",height=500,width=1000,title=f"Total Registeredusers count{year,Qua}")
            # Create Bar chart for PhonePe AppOpen count 
            fig_Appopen=px.bar(user_count_grp,x="State",y="AppOpen_count",color="AppOpen_count",height=500,width=1000,title=f"Total AppOpen count {year,Qua}")
        # Display the bar chart in dashboard
        st.plotly_chart(fig_regi_count)
        st.plotly_chart(fig_Appopen)
    except:
        pass
#======================================State Wise Data Expolaration in stremlit dashboard=============================================
with tab2:

    f1,f2,f3,f4,f5=st.columns([1,1,1,1,1])
    # create selectbox for years
    with f1:
        y1=["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
        
        default_y1 = y1.index("2024")
        year1 = st.selectbox('Year',
                y1,key='Year1',index=default_y1)
        
        if year1=="2018":
            year1=2018
        if year1=="2019":
            year1=2019
        if year1=="2020":
            year1=2020
        if year1=="2021":
            year1=2021
        if year1=="2022":
            year1=2022
        if year1=="2023":
            year1=2023
        if year1=="2024":
            year1=2024
        
    # create selectbox for years   
    with f2:
        q1=["Q1","Q2","Q3","Q4"]

        default_q1=q1.index("Q1")
        Quarter1=st.selectbox("Quarter"
                            ,q1,key="Quarter1",index=default_q1)
        
        if Quarter1=="Q1":
            Quarter1=1
            Qua1="Q1"
        if Quarter1=="Q2":
            Quarter1=2
            if year1==2024:
                st.warning("Data is not Available in Quarter = 2")
                Qua1="Q2" 
        if Quarter1=="Q3":
            Quarter1=3
            if year1==2024:
                st.warning("Data is not Available in Quarter = 3")
                Qua1="Q3"
        if Quarter1=="Q4":
            Quarter1=4 
            if year1==2024:
                st.warning("Data is not Available in Quarter = 4")
                Qua1="Q4"
    # Create selectbox for Explore Data Options
    with f3:
        option_x=["Transactions","User",]
        default_option1=option_x.index("Transactions")
        user_tran1=st.selectbox(" ALL India",option_x,index=default_option1,key="user_tran1")
        if user_tran1=="Transactions":
            user_df2=Map_trans_df
        if user_tran1=="User":
            user_df1=Map_user_df
             
            #=============================Map transaction data Analysis=========================================
    with f4:
        
        # List of state names
        state_names = [
                'Arunachal Pradesh', 'Assam', 'Chandigarh', 'Karnataka', 'Manipur', 'Meghalaya', 'Mizoram',
                'Nagaland', 'Punjab', 'Rajasthan', 'Sikkim', 'Tripura', 'Uttarakhand', 'Telangana', 'Bihar', 'Kerala',
                'Madhya Pradesh', 'Andaman & Nicobar', 'Gujarat', 'Lakshadweep', 'Odisha',
                'Dadra and Nagar Haveli and Daman and Diu', 'Ladakh', 'Jammu & Kashmir', 'Chhattisgarh',
                'Delhi', 'Goa', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Tamil Nadu', 'Uttar Pradesh',
                'West Bengal', 'Andhra Pradesh', 'Puducherry', 'Maharashtra']

        # Sorting the list in ascending order
        sorted_state_names = sorted(state_names)
        # Set a Default state index
        default_state = state_names.index('Tamil Nadu')

        # State selection in Streamlit
        sele_state_name = st.selectbox("Select a State", sorted_state_names, key='state_names', index=default_state)
        
    with f5:
        charts=["Bar chart","Area chart","Line Chart"]
        def_chart=charts.index("Bar chart")
        chart_box=st.selectbox("Select A chart",charts,index=def_chart,key="charts")
    #Load the GeoJSON data for the Indain state
    url2 = "https://raw.githubusercontent.com/pnraj/Projects/master/Phonephe_Pulse/data/test.geojson"

    # Fetching GeoJSON data
    response_1 = requests.get(url2)
    respone=requests.get(url)
    districts_gpd=gpd.read_file(respone.content)
    state_map_fig = districts_gpd.loc[districts_gpd["ST_NM"] == str(sele_state_name), "geometry"]
    # create the subplots for Indian State
    mapfig, ax = plt.subplots(figsize=(90/10, 70/10))
    state_map_fig.plot(ax=ax, facecolor='green', edgecolor='blue')
    ax.axis('off')

    try:# filter the data based on specified year and quarter
        filter_tran=user_df2[(user_df2["State"]==sele_state_name)&(user_df2["Year"]== year1)&(user_df2["Quarter"]==Quarter1)]
        filter_tran_sorted = filter_tran.sort_values(by=["Transation_amount","Transation_count"], ascending=True)
        cl1,cl2=st.columns([1,2])
        # Display the results in dashboard
        with cl1:
            st.pyplot(mapfig)
            st.markdown(":green[India]")
            st.subheader(sele_state_name)
            st.markdown(":green[All Transactions]")
            sum_tra_cou=filter_tran_sorted["Transation_count"].sum()
            st.subheader(format_number1(sum_tra_cou))
            st.markdown(":green[Total Payment Value]")
            sum_tra_amou=filter_tran["Transation_amount"].sum()
            st.subheader(mcrores(sum_tra_amou))
            st.markdown(":green[Avg.Transaction Value]")
            st.subheader(format_number(sum_tra_amou/sum_tra_cou))

        with cl2:
            # Create bar chart for transaction amount
            if chart_box=="Bar chart":
                bar_fig_amount=px.bar(filter_tran_sorted,x="Transation_amount",y="District_name",orientation="h",
                            height=800,width=700,title=f"Transaction Amount in the state of {sele_state_name} for {year1,Qua1}",
                            color="Transation_amount",  # Color by transaction amount
                            labels={"Transaction_amount": "Amount", "District_name": "District"})
                # Create bar chart for transaction count
                bar_fig_coun=px.bar(filter_tran_sorted,x="Transation_count",y="District_name",orientation="h",
                            height=800,width=700,title=f"Transaction Count in the state of {sele_state_name} for {year1,Qua1}",
                            color="Transation_count",  # Color by transaction amount
                            labels={"Transation_count": "Count", "District_name": "District"})
                # Display the results in streamlit dashboard
                st.plotly_chart(bar_fig_amount)
                st.plotly_chart(bar_fig_coun)

            elif chart_box=="Area chart":
                # Create area chart for transaction amount
                Area_fig_amou=px.area(filter_tran,x="District_name",y="Transation_amount",
                            height=800,width=700,title=f"Transaction Amount in the state of {sele_state_name} for {year1,Qua1}",
                            color="Transation_amount",  # Color by transaction amount
                            labels={"Transaction_amount": "Amount", "District_name": "District"})
                # Create area chart for transaction count
                area_fig_coun=px.area(filter_tran,x="District_name",y="Transation_count",
                            height=800,width=700,title=f"Transaction Count in the state of {sele_state_name} for {year1,Qua1}",
                            color="Transation_count",  # Color by transaction amount
                            labels={"Transation_count": "Count", "District_name": "District"})
                # Display the results in streamlit dashboard
                st.plotly_chart(Area_fig_amou)
                st.plotly_chart(area_fig_coun)
            elif chart_box=="Line Chart":
                # Create Line chart for transaction Amount
                line_fig_amou=px.line(filter_tran,x="District_name",y="Transation_amount",
                            height=800,width=700,title=f"Transaction Amount in the state of {sele_state_name} for {year1,Qua1}",
                            labels={"Transaction_amount": "Amount", "District_name": "District"})
                # Create line chart for transaction count
                line_fig_coun=px.line(filter_tran,x="District_name",y="Transation_count",
                            height=800,width=700,title=f"Transaction Count in the state of {sele_state_name} for {year1,Qua1}",
                            labels={"Transation_count": "Count", "District_name": "District"})
                # Display the results in streamlit dashboard
                st.plotly_chart(line_fig_amou)
                st.plotly_chart(line_fig_coun)
    except:
        pass
            #============================Map User data Analysis=============================
    try:# filter the data based on specified year and quarter   
        filter_user=user_df1[(user_df1["State"]==sele_state_name)&(user_df1["Year"]== year1)&(user_df1["Quarter"]==Quarter1)]  
        filter_user_sort = filter_user.sort_values(by=["Registeredusers_count"], ascending=True)
        filter_user_sorted=filter_user.sort_values(by=["AppOpen_count"],ascending=True)
        # Display the results in streamlit dashboard
        cu1,cu2=st.columns([1,2])
        with cu1:
            st.pyplot(mapfig)
            st.markdown(":green[India]")
            st.subheader(sele_state_name)
            sum_user_reg=filter_user_sorted["Registeredusers_count"].sum()
            st.markdown(":green[Registered PhonePe users till "f"{Qua1},{year1}]")
            st.subheader(format_number1(sum_user_reg))
            sum_user_cou=filter_user_sorted["AppOpen_count"].sum()
            st.markdown(":green[PhonePe app opens in "f"{Qua1},{year1}] ")
            st.subheader(format_number1(sum_user_cou))
        
        with cu2:
            if chart_box=="Bar chart":
                    # Create bar chart for Registeredusers_count
                    bar_fig_reg=px.bar(filter_user_sort,x="Registeredusers_count",y="District_name",orientation="h",
                                height=800,width=700,title=f"Registered users count in the state of {sele_state_name} for {year1,Qua1}",
                                color="Registeredusers_count",  # Color by transaction amount
                                labels={"Registeredusers_count": "Count", "District_name": "District"})
                    # Create bar chart for AppOpen_count
                    bar_fig_apopen=px.bar(filter_user_sorted,x="AppOpen_count",y="District_name",orientation="h",
                                height=800,width=700,title=f"AppOpen count in the state of {sele_state_name} for {year1,Qua1}",
                                color="AppOpen_count",  # Color by transaction amount
                                labels={"AppOpen_count": "Count", "District_name": "District"})
                    # Display the results in streamlit dashboard
                    st.plotly_chart(bar_fig_reg)
                    st.plotly_chart(bar_fig_apopen)
            elif chart_box=="Area chart":
                    # Create area chart for Registeredusers_count
                    Area_fig_regi=px.area(filter_user,x="District_name",y="Registeredusers_count",
                                height=800,width=700,title=f"Registeredusers count in the state of {sele_state_name} for {year1,Qua1}",
                                color="Registeredusers_count",  # Color by transaction amount
                                labels={"Registeredusers_count": "Count", "District_name": "District"})
                    # Create area chart for AppOpen_count
                    area_fig_Apopen=px.area(filter_user,x="District_name",y="AppOpen_count",
                                height=800,width=700,title=f"AppOpen count in the state of {sele_state_name} for {year1,Qua1}",
                                color="AppOpen_count",  # Color by transaction amount
                                labels={"AppOpen_count": "Count", "District_name": "District"})
                    # Display the results in streamlit dashboard
                    st.plotly_chart(Area_fig_regi)
                    st.plotly_chart(area_fig_Apopen)
            elif chart_box=="Line Chart":
                    # Create line chart for Registeredusers_count
                    line_fig_regi=px.line(filter_user,x="District_name",y="Registeredusers_count",
                                height=800,width=700,title=f"Registeredusers count in the state of {sele_state_name} for {year1,Qua1}",
                                labels={"Registeredusers_count": "Amount", "District_name": "District"})
                    # Create line chart for AppOpen_count
                    line_fig_apope=px.line(filter_user,x="District_name",y="AppOpen_count",
                                height=800,width=700,title=f"AppOpen count in the state of {sele_state_name} for {year1,Qua1}",
                                labels={"AppOpen_count": "Count", "District_name": "District"})
                    # Display the results in streamlit dashboard
                    st.plotly_chart(line_fig_regi)
                    st.plotly_chart(line_fig_apope)
    except:
        pass
#==========================================Insights part streamlit dashboard===========================================
with tab3:
    # Create 10 different Query
    query=["1.Track the Overall Transaction Volume Over a year",
            "2.Track the Overall Transaction Volume Over a each Quarter",
            "3.The total number of PhonePe users and their distribution across different mobile brands last 5 yaers",
            "4.Total Transaction Volume by Categories wise",
            "5.Top 10 states with the highest Transaction Count for the year",
            "6.Top 10 states with the highest Transaction Amount for the year",
            "7.Top 10 states with the Lowest Transaction Amount for the year",
            "8.Growth of Registered User Count for the Past 5 Years",
            "9.Top 10 district with the highest Transaction Amount for the year",
            "10.Top 10 district with their Lowest Transaction Amount for the year"]
    #Create Selectbox for 10 Querys
    Query_sele=st.selectbox("Select a Query",query)
    # Query 1 execute 
    if Query_sele=="1.Track the Overall Transaction Volume Over a year":
        overall_trans_year=Map_trans_df.groupby("Year")["Transation_count"].sum()
        overall_trans_year=Map_trans_df.groupby("Year")["Transation_count"].sum()
        df_overall_trans_year=pd.DataFrame(overall_trans_year).reset_index()
        upto_2023=df_overall_trans_year[df_overall_trans_year["Year"]!=2024]
        # Create line chart for Transaction Count
        fig_tran_over=px.line(upto_2023,x="Year",y="Transation_count",
                            height=500,width=800,
                            labels={"Transation_count":" Overall Transaction Count","Year":"Year"},
                            title="Overall Transaction Volume Over a year"
                            )
        # Display the results in streamlit dashboard
        w1,w2=st.columns([2.5,1])
        with w1:
            st.plotly_chart(fig_tran_over)
        with w2:
            st.write(upto_2023)
        st.text(""" This dashboard provides an overview of the transaction volumes over the years. 
                    You can explore how transaction volumes have changed from 2018 to 2024. 
                    The data is visualized in a line chart for easier analysis.""")
    # Query 2 execute 
    if  Query_sele=="2.Track the Overall Transaction Volume Over a each Quarter":
        overall_trans_year=Map_trans_df.groupby(["Year","Quarter"])["Transation_count"].sum()
        df_overall_trans_year=pd.DataFrame(overall_trans_year).reset_index()
        df_overall_trans_year['Year_Quarter'] = df_overall_trans_year['Year'].astype(str) + ' Q' + df_overall_trans_year['Quarter'].astype(str)
        fig_te=px.bar(df_overall_trans_year,x="Year_Quarter",y="Transation_count",title="Transaction Count by Year and Quarter",
                        color="Transation_count")
        st.plotly_chart(fig_te) 
    # Query 3 execute 
    if Query_sele=="3.The total number of PhonePe users and their distribution across different mobile brands last 5 yaers":
        year2=st.selectbox("Select the Year",[2018, 2019, 2020, 2021, 2022, 2023])
        filtering_table=Agg_user_df[(Agg_user_df["Year"]==year2)]
        filtering_grop=filtering_table.groupby("Brand_name")["User_count"].sum().reset_index()
        filtering_sort=filtering_grop.sort_values(by=["User_count"],ascending=False)
        mobile_df_fig=px.bar(filtering_sort,x="Brand_name",y="User_count",color="User_count",title=f"Phonepe user mobile brand Count in the year of{year2}")
        st.plotly_chart(mobile_df_fig)
    # Query 4 execute 
    if Query_sele=="4.Total Transaction Volume by Categories wise":
        op1,op2=st.columns(2)
        with op1:
            year2=st.selectbox("Select the Year",[2018, 2019, 2020, 2021, 2022, 2023,2024])
        with op2:
            Quarter2=st.selectbox("Select the Quarter",[1,2,3,4])
        filter_table2=Agg_trans_df[(Agg_trans_df["Year"]==year2)&(Agg_trans_df["Quarter"]==Quarter2)]
        filter_table2_gro=filter_table2.groupby("Transation_type")["Transation_count"].sum().reset_index()
        type_pay_fig=px.pie(filter_table2_gro,values="Transation_count",hover_name="Transation_type",color="Transation_count",title=f"Transaction Volume by Categeris wise {year2 , Quarter2}",names="Transation_type")
        st.plotly_chart(type_pay_fig)
     # Query 5 execute 
    if Query_sele=="5.Top 10 states with the highest Transaction Count for the year":
        op1,op2=st.columns(2)
        with op1:
            year2=st.selectbox("Select the Year",[2018, 2019, 2020, 2021, 2022, 2023,2024])
        with op2:
            Quarter2=st.selectbox("Select the Quarter",[1,2,3,4])
        filter_table3=Top_trans_df[(Top_trans_df["Year"]==year2)& (Top_trans_df["Quarter"]==Quarter2)]
        filter_table3_gro=filter_table3.groupby("State")["Transation_count"].sum().reset_index()
        filter_table3_sort=filter_table3_gro.sort_values(by=["Transation_count"],ascending=False).head(10)
        filter_table3_df=pd.DataFrame(filter_table3_sort).reset_index(drop=False).drop(columns="index")
        filter_table3_df["Transation_count"]=filter_table3_df["Transation_count"].apply(format_number1)
        fig_top=px.pie(filter_table3_sort,values="Transation_count",hover_name="State",
                    title=f"Top 10 highest Transaction Count by State for the Year{year2,Quarter2}",names="State")
        w5,w6=st.columns([2.5,1])
        with w5:
            st.plotly_chart(fig_top)
        with w6:
            st.dataframe(filter_table3_df)
    # Query 6 execute    
    if Query_sele=="6.Top 10 states with the highest Transaction Amount for the year":
        op1,op2=st.columns(2)
        with op1:
            year2=st.selectbox("Select the Year",[2018, 2019, 2020, 2021, 2022, 2023,2024])
        with op2:
            Quarter2=st.selectbox("Select the Quarter",[1,2,3,4])
        filter_table4=Top_trans_df[(Top_trans_df["Year"]==year2)& (Top_trans_df["Quarter"]==Quarter2)]
        filter_table4_gro=filter_table4.groupby("State")["Transation_amount"].sum().reset_index()
        filter_table4_sort=filter_table4_gro.sort_values(by=["Transation_amount"],ascending=False).head(10)
        filter_table4_df=pd.DataFrame(filter_table4_sort).reset_index(drop=False).drop(columns="index")
        filter_table4_df["Transation_amount"]=filter_table4_df["Transation_amount"].apply(mcrores)
        fig_top1=px.pie(filter_table4_sort,values="Transation_amount",hover_name="State",
                    title=f"Top 10 highest Transaction Amounts by State for the Year{year2,Quarter2}",names="State")
        w3,w4=st.columns([2.5,1])
        with w3:
            st.plotly_chart(fig_top1)
        with w4:
            st.dataframe(filter_table4_df) 
    # Query 7 execute 
    if Query_sele=="7.Top 10 states with the Lowest Transaction Amount for the year":
        op1,op2=st.columns(2)
        with op1:
            year2=st.selectbox("Select the Year",[2018, 2019, 2020, 2021, 2022, 2023,2024])
        with op2:
            Quarter2=st.selectbox("Select the Quarter",[1,2,3,4])
        filter_table7=Top_trans_df[(Top_trans_df["Year"]==year2)& (Top_trans_df["Quarter"]==Quarter2)]
        filter_table7_gro=filter_table7.groupby("State")["Transation_amount"].sum().reset_index()
        filter_table7_sort=filter_table7_gro.sort_values(by=["Transation_amount"],ascending=True).head(10)
        filter_table7_df=pd.DataFrame(filter_table7_sort).reset_index(drop=False).drop(columns="index")
        filter_table7_df["Transation_amount"]=filter_table7_df["Transation_amount"].apply(mcrores)
        fig_top7=px.bar(filter_table7_sort,x="State",y="Transation_amount",color="Transation_amount",      
                        title=f"Top 10 states with their Lowest Transaction Amounts for the Year{year2,Quarter2}")
        w3,w4=st.columns([2.5,1])
        with w3:
            st.plotly_chart(fig_top7)
        with w4:
            st.dataframe(filter_table7_df)
    # Query 8 execute 
    if Query_sele=="8.Growth of Registered User Count for the Past 5 Years":
        user_growth=Map_user_df.groupby("Year")["Registeredusers_count"].sum()
        user_growth_df=pd.DataFrame(user_growth)
        user_growth_df.reset_index(inplace=True)
        fiter_user_groth=user_growth_df[user_growth_df["Year"]!=2024]
        grow_fig=px.bar(fiter_user_groth,x="Year",y="Registeredusers_count",color="Registeredusers_count",title="Growth of Registered User Count for the Past 5 Years")
        st.plotly_chart(grow_fig)
    # Query 9 execute 
    if Query_sele=="9.Top 10 district with the highest Transaction Amount for the year":
        op1,op2=st.columns(2)
        with op1:
            year2=st.selectbox("Select the Year",[2018, 2019, 2020, 2021, 2022, 2023,2024])
        with op2:
            Quarter2=st.selectbox("Select the Quarter",[1,2,3,4])
        filter_table5=Top_trans_df[(Top_trans_df["Year"]==year2)& (Top_trans_df["Quarter"]==Quarter2)]
        filter_table5_gro=filter_table5.groupby("District_name")["Transation_amount"].sum().reset_index()
        filter_table5_sort=filter_table5_gro.sort_values(by=["Transation_amount"],ascending=False).head(10)
        filter_table5_df=pd.DataFrame(filter_table5_sort).reset_index(drop=True)
        filter_table5_df["Transation_amount"]=filter_table5_df["Transation_amount"].apply(mcrores)
        fig_tab5=px.bar(filter_table5_sort,x="District_name",y="Transation_amount",color="Transation_amount",
                        title=f"Top 10 district with the highest Transaction Amount for the year{year2,Quarter2}")
        w3,w4=st.columns([2.5,1])
        with w3:
            st.plotly_chart(fig_tab5)
        with w4:
            st.dataframe(filter_table5_df)
    # Query 10  execute 
    if Query_sele=="10.Top 10 district with their Lowest Transaction Amount for the year":
        op1,op2=st.columns(2)
        with op1:
            year2=st.selectbox("Select the Year",[2018, 2019, 2020, 2021, 2022, 2023,2024])
        with op2:
            Quarter2=st.selectbox("Select the Quarter",[1,2,3,4])
        filter_table6=Top_trans_df[(Top_trans_df["Year"]==year2)& (Top_trans_df["Quarter"]==Quarter2)]
        filter_table6_gro=filter_table6.groupby("District_name")["Transation_amount"].sum().reset_index()
        filter_table6_sort=filter_table6_gro.sort_values(by=["Transation_amount"],ascending=True).head(10)
        filter_table6_df=pd.DataFrame(filter_table6_sort).reset_index(drop=True)
        filter_table6_df["Transation_amount"]=filter_table6_df["Transation_amount"].apply(mcrores)
        fig_tab6=px.bar(filter_table6_sort,x="District_name",y="Transation_amount",color="Transation_amount",
                    title=f"Top 10 district with their Lowest Transaction Amount for the year{year2,Quarter2}")
        w3,w4=st.columns([2.5,1])
        with w3:
            st.plotly_chart(fig_tab6)
        with w4:
            st.dataframe(filter_table6_df)
        


         

