import pathlib
from bs4 import BeautifulSoup
import logging
import shutil
import streamlit as st
import pandas as pd

def inject_ga():
    GA_ID = "google_analytics"

    GA_JS = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-9CFV9EV1CE"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-9CFV9EV1CE');
    </script>
    """

    # Insert the script in the head tag of the static template inside your virtual
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    logging.info(f'editing {index_path}')
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(id=GA_ID):  # if cannot find tag
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  # recover from backup
        else:
            shutil.copy(index_path, bck_index)  # keep a backup
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_JS)
        index_path.write_text(new_html)


inject_ga()


st.set_page_config(page_title="Python Search Engine", page_icon="🐍", layout="wide")
st.title("Python Search Engine")
st.markdown("""
    Lorem ipsum dolor sit amet. Qui inventore corporis 33 temporibus tempora eos atque quia ex vero aspernatur eum voluptas internos. Et omnis modi At magnam impedit a labore omnis At accusantium debitis est consequatur voluptas. Vel dolorem quasi aut nesciunt atque et totam illo non tempora quae vel expedita consequatur in quibusdam quia. Rem dolore quisquam rem alias nulla eum quae eveniet eum minus blanditiis.

    Qui Quis necessitatibus aut molestias corporis et voluptatem odit. Qui libero dolore et atque enim et libero molestiae ea doloremque reiciendis non beatae voluptas ut repellat exercitationem qui nemo nemo.

    At voluptates consequuntur sed saepe amet et corporis facilis vel iusto atque qui aspernatur commodi qui eius amet et ipsa quae? Ut sint delectus ut officia perferendis a possimus illum in facilis omnis vel blanditiis temporibus et quia nihil! Et porro voluptatem ea nostrum enim est nesciunt eaque. Sed galisum exercitationem id doloribus dolore et aperiam commodi ab minus magnam non ducimus tenetur 33 sint quia ut nihil autem.
    """)

df = pd.read_csv("spreadsheet.csv").fillna("")

text_search = st.text_input("Search videos by title or speaker", value="")

m1 = df["Autor"].str.contains(text_search)
m2 = df["Título"].str.contains(text_search)
df_search = df[m1 | m2]


#if text_search:
     #st.write(df_search)

# Show the cards
N_cards_per_row = 3
if text_search:
    for n_row, row in df_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{row['Evento'].strip()} - {row['Lugar'].strip()} - {row['Fecha'].strip()} ")
            st.markdown(f"**{row['Autor'].strip()}**")
            st.markdown(f"*{row['Título'].strip()}*")
            st.markdown(f"**{row['Video']}**")
