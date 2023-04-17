import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

DB_USER = "deliverable_taskforce"
DB_PASSWORD = "learn_sql_2023"
DB_HOSTNAME = "training.postgres.database.azure.com"
DB_NAME = "deliverable"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:5432/{DB_NAME}")
result = engine.execute("SELECT 1")
result.first()

st.title("The number of reviews per day in Amsterdam,Groningen and Rotterdam")
df = pd.read_sql_query(
    """
  select
	date(r.datetime) as day,
	COUNT(r.restaurant_id),
	r2.location_city 
from
	reviews r
inner join restaurants r2 
on
	r2.restaurant_id = r.restaurant_id
where
	r2.location_city in ('Rotterdam','Amsterdam', 'Groningen') and r.datetime > '2022-01-01' and r.datetime < '2023-01-01'
group by
	day, r2.location_city 
order by
	day asc
    """,
    con=engine,
)
fig1 = px.line(df, x="day", y="count", color="location_city")
st.plotly_chart(fig1)
start_year1 = df["day"].min()
end_year1 = df["day"].max()


selected_date1 = st.slider("Date", start_year1, end_year1, start_year1)
filtered_data1 = df[df["day"] == selected_date1]
st.write("Filtered Data:")
st.dataframe(filtered_data1)


def second():
    st.title("The number of covid infections per day in Amsterdam, Groningen and Rotterdam")
    df2 = pd.read_sql_query(
        """
		select
			mtd.total_reported,
			mtd.date_of_publication as date,
			mtd.municipality_name as city
		from
			municipality_totals_daily mtd
		where
			mtd.municipality_name in ('Rotterdam', 'Amsterdam', 'Groningen')
			and mtd.date_of_publication > '2022-01-01'
			and mtd.date_of_publication < '2023-01-01'
		""",
        con=engine,
    )
    fig2 = px.line(df2, x="date", y="total_reported", color="city")
    st.plotly_chart(fig2)
    start_year = df2["date"].min()
    end_year = df2["date"].max()

    selected_date = st.slider("Date", start_year, end_year, start_year)
    filtered_data = df2[df2["date"] == selected_date]
    st.write("Filtered Data:")
    st.dataframe(filtered_data)


def main():
    second()


if __name__ == "__main__":
    main()
