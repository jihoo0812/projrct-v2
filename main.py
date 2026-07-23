import streamlit as st
import pandas as pd

# ------------------------------------------------------------------
# 데이터: "Top of levels by number of frame perfects - FPLL" PDF에서 추출
# 각 항목: 레벨명, FPS60, FPS120, FPS240, Rating(점수), Status, ID, Comment
# ------------------------------------------------------------------
RAW_DATA = [
    ("Aeternus", 212, 78, 3, 380, "U", "102646926", ""),
    ("Africa Circles (unnerfed)", 170, 35, None, 240, "U", "67153243", "Release at 47% is incredibly hard"),
    ("CorroZ", 127, 46, None, 219, "U", "86191664", ""),
    ("Tidal Wave", 200, 1, None, 202, "R", "86407629", ""),
    ("Society", 128, 27, 3, 194, "R", "127323087", ""),
    ("Amethyst", 143, 13, 2, 177, "R", "119550490", "The first click is not possible on 120 FPS"),
    ("Ashley Wave Trials", 155, 11, None, 177, "R", "62912799", ""),
    ("Green Bullet", 163, 7, None, 177, "R", "142896409", ""),
    ("Natural Disaster (unnerfed)", 120, 22, None, 164, "U", "85176381", "For 60 FPS dash blocks at 59% and 89-90% were fixed"),
    ("Azure Flare (Aeden's)", 109, 23, 2, 163, "U", "80518698", "It's possible on 60 FPS (with super lucky frames alignment)"),
    ("KOCMOC (old unnerfed)", 114, 19, 2, 160, "U", "private", "One timing on ball is incredibly hard"),
    ("Thinking Space II", 108, 20, 1, 152, "R", "119544028", ""),
    ("Sarai", 59, 21, 10, 141, "U", "private", "First ball is incredibly hard"),
    ("Eternal Night (old)", 107, 16, None, 139, "U", "73011766", "For 60 FPS dash blocks on first wave were fixed"),
    ("Antarctic Lights", 106, 16, None, 138, "V", "144988390", ""),
    ("KOCMOC (old nerfed)", 100, 11, None, 122, "U", "69196070", ""),
    ("Exasperation", 83, 13, 2, 117, "U", "31325851", "For 60 FPS yellow orb at 17% was fixed"),
    ("Tremor", 75, 18, 1, 115, "C", "79823052", ""),
    ("Defeated Circles", 101, 6, None, 113, "R", "120012581", ""),
    ("WOODKID (unnerfed)", 77, 13, 2, 111, "U", "70581105", "Bugs at 17%, 42% and 82% were fixed"),
    ("FINAL FANTASY", 32, 27, 5, 106, "C", "76767195", "Play on 144 or 240 FPS"),
    ("Unknown (old)", 58, 18, 3, 106, "U", "70003258", ""),
    ("Lesopowal", 88, 7, None, 102, "V", "137886942", ""),
    ("Nullscapes", 82, 9, None, 100, "R", "109780665", ""),
    ("Aquamarine", 89, 6, None, 101, "V", "77331805", ""),
    ("Penumbral", 73, 11, 1, 99, "R", "134942736", ""),
    ("The Bloop", 95, 1, None, 97, "R", "135661111", ""),
    ("Andromeda", 84, 6, None, 96, "R", "114283297", ""),
    ("Delirium", 61, 14, None, 89, "C", "68839068", ""),
    ("EXPIRATION DATE", 69, 10, None, 89, "C", "95357570", ""),
    ("Solar Flare", 89, None, None, 89, "R", "90390075", ""),
    ("Alpha Never Clear", 68, 9, None, 86, "U", "private", ""),
    ("Avernus", 82, 2, None, 86, "R", "89496627", ""),
    ("Every End", 82, 2, None, 86, "R", "116174063", ""),
    ("Re", 27, 21, 4, 85, "C", "126279500", ""),
    ("Bosco busch", 55, 14, None, 83, "C", "95259962", ""),
    ("Wocky circles", 71, 6, None, 83, "V", "100420930", ""),
    ("Stercore", 49, 16, None, 81, "C", "69766474", ""),
    ("SADOMASOCHISM", 59, 11, None, 81, "C", "76213334", ""),
    ("Quanteuse processing", 65, 5, 1, 79, "R", "113710822", ""),
    ("Acheron", 63, 8, None, 79, "R", "73667628", ""),
    ("Subsuming Vortex", 60, 8, None, 76, "R", "127997391", ""),
    ("Silent Acropolis (unnerfed)", 39, 14, 2, 75, "U", "34506120", "Second jump and one timing on ufo are incredibly hard"),
    ("Slaughterhouse", 65, 4, None, 73, "R", "27690100", ""),
    ("Silent clubstep (unnerfed)", 28, 14, 4, 72, "U", "38692301", "Swag route at 15% was used"),
    ("Flamewall", 71, None, None, 71, "R", "126242564", ""),
    ("Silent Clubstep II", 40, 13, 1, 70, "U", "78614226", "The lower path at the end was used"),
    ("MINUS WORLD", 68, 1, None, 70, "U", "77875682", "For 60 FPS bugs at 20%, 37% and 92% were fixed, for 120 FPS - only at 20%"),
    ("VSC", 61, 3, None, 67, "C", "60805571", ""),
    ("Sakupen Circles", 47, 9, None, 65, "R", "76962930", ""),
    ("Aztec rave monkey", 64, None, None, 64, "C", "112667786", "60 FPS only"),
    ("Warcora", 63, None, None, 63, "U", "68898570", "60 FPS only"),
    ("Old Orochi", 48, 5, 1, 62, "U", "59231857", ""),
    ("521", 24, 19, None, 62, "C", "85701165", ""),
    ("Murder Mitten", 50, 6, None, 62, "C", "81973761", ""),
    ("Oblivers", 56, 3, None, 62, "C", "85042202", "For 60 and 120 FPS bug at 12% was fixed"),
    ("Subterminal Point", 51, 4, None, 59, "R", "113599729", ""),
    ("Natural Disaster (old)", 57, 1, None, 59, "V", "76483916", ""),
    ("3SH in Hell", 58, None, None, 58, "C", "61614466", "60 FPS only"),
    ("Sevvend Clubstep", 58, None, None, 58, "R", "120255728", ""),
    ("INNARDS (unnerfed)", 33, 12, None, 57, "V", "54496752", "For 120 FPS blue orb at 60% was fixed"),
    ("KOCMOC", 54, 1, None, 56, "R", "87665224", "For 60 FPS bugs at 5%, 55% and 61% were fixed"),
    ("Lightposts", 35, 8, 1, 55, "C", "73199960", ""),
    ("Blood Echo", 55, None, None, 55, "R", "112242564", ""),
    ("Anathema", 52, 1, None, 54, "R", "112313819", ""),
    ("ORBIT", 52, 1, None, 54, "R", "133175713", ""),
    ("Abyss of Darkness", 43, 5, None, 53, "R", "49896559", ""),
    ("Apotheosis", 51, 1, None, 53, "C", "76663114", ""),
    ("Tunnel of Despair", 50, 1, None, 52, "R", "91351939", ""),
    ("Aerial Gleam", 52, None, None, 52, "R", "79771070", ""),
    ("Trotil (old)", 43, 4, None, 51, "U", "82939238", ""),
    ("Spectre", 51, None, None, 51, "R", "110815379", ""),
    ("Poocubed", 48, 1, None, 50, "R", "85133223", "For 60 FPS red orb at 58% was fixed"),
    ("ETERNALtheory", 48, 1, None, 50, "V", "92196326", ""),
    ("Voltage", 41, 4, None, 49, "R", "131599104", ""),
    ("My backyard", 49, None, None, 49, "C", "116618684", "60 FPS only"),
    ("Illusion of Hell", 42, 3, None, 48, "C", "38230726", ""),
    ("Mayhem", 44, 2, None, 48, "R", "82544060", ""),
    ("Sonic Wave Infinity", 46, 1, None, 48, "R", "69685815", ""),
    ("Menace", 48, None, None, 48, "R", "107805281", ""),
    ("The Plunge", 43, 2, None, 47, "R", "113220284", ""),
    ("MINUSdry", 44, 1, None, 46, "R", "89414220", ""),
    ("The Salt Factory", 44, 1, None, 46, "R", "113045735", ""),
    ("Saul Goodman", 45, None, None, 45, "R", "90477539", "For 60 FPS bug at 59% was fixed"),
    ("Flutterwonder", 30, 7, None, 44, "C", "65496433", ""),
    ("Edge of Destiny", 42, 1, None, 44, "R", "89187968", ""),
    ("Silentlocked", 37, 3, None, 43, "R", "113959291", ""),
    ("KOSETSU", 39, 2, None, 43, "R", "109439644", ""),
    ("Walter white", 43, None, None, 43, "R", "81011195", ""),
    ("Anodyne", 43, None, None, 43, "C", "105191372", ""),
    ("Centipede (old)", 43, None, None, 43, "V", "106646765", ""),
    ("UNKNOWN", 32, 5, None, 42, "R", "88203501", ""),
    ("Deorum", 36, 3, None, 42, "C", "55392313", ""),
    ("CHIL", 42, None, None, 42, "R", "114281093", ""),
    ("Silent poltergeist", 37, 2, None, 41, "V", "13586257", ""),
    ("Delusion", 39, 1, None, 41, "C", "65348932", ""),
    ("M I S F O R T U N E", 30, 5, None, 40, "V", "115093521", ""),
    ("THE ROCK HOUSE (unnerfed)", 38, 1, None, 40, "U", "83397107", ""),
    ("COMBUSTION", 40, None, None, 40, "R", "94359172", ""),
    ("Amalgam", 40, None, None, 40, "R", "95675702", ""),
    ("EVIL", 40, None, None, 40, "C", "110453861", "60 FPS only"),
    ("Silent clubstep", 29, 5, None, 39, "R", "4125776", ""),
    ("qoUEO", 35, 2, None, 39, "R", "81721025", ""),
    ("Deadlier Clubstep", 38, None, None, 38, "R", "96314787", ""),
    ("Through The Gates", 27, 5, None, 37, "R", "49072489", ""),
    ("Falling Illusion", 27, 5, None, 37, "C", "50542904", ""),
    ("Oblivion", 35, 1, None, 37, "R", "71025973", ""),
    ("The Wonder of You", 37, None, None, 37, "R", "94858072", ""),
    ("Craven Soul", 30, 3, None, 36, "C", "67862379", ""),
    ("KOCMOC (Trick's)", 34, 1, None, 36, "V", "89653463", "For 60 FPS bugs at 55%, 61% and 83% were fixed, for 120 FPS - only at 55%"),
    ("Climax", 34, 1, None, 36, "R", "95049815", ""),
    ("Belladonna", 36, None, None, 36, "R", "94969889", "For 2.2 bug at 85% was fixed"),
    ("Levigo", 33, 1, None, 35, "R", "97086864", ""),
    ("Deimos", 35, None, None, 35, "R", "93091893", "For 60 FPS bugs at 18% and 88% were fixed"),
    ("BOOBAWAMBA", 31, 1, None, 33, "R", "110816181", ""),
    ("BRITNEY NO SCLEARS", 33, None, None, 33, "R", "125317359", ""),
    ("CONVULSION", 30, 1, None, 32, "R", "113322063", ""),
    ("Gaggatrondra", 32, None, None, 32, "R", "114990369", ""),
    ("Stellar Night", 29, 1, None, 31, "R", "83244159", ""),
    ("Collapse", 31, None, None, 31, "R", "113256247", ""),
    ("The Hallucination", 30, None, None, 30, "R", "81139702", ""),
    ("Element 111 Rg", 17, 4, 1, 29, "V", "61775814", ""),
    ("The Lightning Rod", 27, 1, None, 29, "R", "93917076", ""),
    ("Shardscapes", 29, None, None, 29, "R", "79997992", ""),
    ("THE ROCK HOUSE", 29, None, None, 29, "V", "83828637", ""),
    ("Paraballa", 28, None, None, 28, "C", "68963370", "60 FPS only"),
    ("NEUTRA", 25, 1, None, 27, "R", "88611404", "For 120 FPS bug at 45% was fixed"),
    ("Hell Ball Finale", 27, None, None, 27, "C", "86047466", "60 FPS only"),
    ("Arcturus", 26, None, None, 26, "R", "72315402", ""),
    ("PSYCHOPATH", 26, None, None, 26, "R", "103925676", ""),
    ("Congregation", 23, 1, None, 25, "R", "68668045", ""),
    ("Cosmic Cyclone", 25, None, None, 25, "R", "76159410", ""),
    ("Nautical Nebula", 25, None, None, 25, "V", "110891882", ""),
    ("Snowbound", 25, None, None, 25, "R", "120289520", ""),
    ("Tartarus", 22, 1, None, 24, "R", "59075347", ""),
    ("Cobwebs", 24, None, None, 24, "R", "82172844", ""),
    ("Firework", 23, None, None, 23, "R", "75206202", "For 60 FPS first cube was fixed"),
    ("Trueffet", 20, 1, None, 22, "R", "71434979", ""),
    ("The Golden", 22, None, None, 22, "R", "60978746", ""),
    ("Kyouki", 22, None, None, 22, "R", "86018142", "For 60 FPS bug at 66% was fixed"),
    ("RUTHLESS (unnerfed)", 21, None, None, 21, "V", "86154347", "For 60 FPS bug at 62% was fixed"),
    ("RUST", 19, None, None, 19, "R", "71912451", ""),
    ("Diabolic ClubStep", 19, None, None, 19, "R", "73214186", ""),
    ("LIMBO", 19, None, None, 19, "R", "86084399", ""),
    ("Midnight", 19, None, None, 19, "R", "96083028", ""),
    ("The Yangire", 19, None, None, 19, "R", "110500920", ""),
    ("Thinking Space", 13, 2, None, 17, "R", "54953085", "For 60 FPS bug at 30% was fixed"),
    ("SUPERHATEMEWORLD", 12, 2, None, 16, "R", "57571983", "For 60 FPS first jump and yellow orb at 89% were fixed"),
    ("Trotil", 14, 1, None, 16, "R", "94578424", ""),
    ("Cimmerian Shade", 16, None, None, 16, "R", "93340783", ""),
    ("Apocalyptic Trilogy", 16, None, None, 16, "R", "113443235", ""),
    ("Hard Machine", 13, 1, None, 15, "R", "72744364", ""),
    ("Based After Based", 15, None, None, 15, "R", "110534288", ""),
    ("Promethean", 14, None, None, 14, "R", "69333212", ""),
    ("Kowareta", 11, 1, None, 13, "R", "46763581", ""),
    ("Zodiac", 13, None, None, 13, "R", "52374843", ""),
    ("Hatred", 12, None, None, 12, "R", "27580467", ""),
    ("Lucid Nightmares", 12, None, None, 12, "R", "52310333", "For 60 FPS bugs at 50% and 56% were fixed"),
    ("Shukketsu", 12, None, None, 12, "R", "75286957", ""),
    ("Verdant Landscape", 12, None, None, 12, "R", "76543324", ""),
    ("Eyes in the Water", 10, None, None, 10, "R", "95851008", ""),
]

COLUMNS = ["Level", "60 FPS", "120 FPS", "240 FPS", "Rating", "Status", "ID", "Comment"]

STATUS_LABELS = {
    "R": "Rated, verified",
    "V": "Unrated, verified",
    "U": "Unverified",
    "C": "Challenge, verified",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.DataFrame(RAW_DATA, columns=COLUMNS)
    # 알파벳순 정렬 (대소문자 무시)
    df["_sort_key"] = df["Level"].str.lower()
    df = df.sort_values("_sort_key").drop(columns="_sort_key").reset_index(drop=True)
    return df


def main() -> None:
    st.set_page_config(page_title="FPLL - Frame Perfect Levels (A-Z)", page_icon="🎮", layout="wide")

    st.title("🎮 Top of Levels by Number of Frame Perfects (FPLL)")
    st.caption(
        "원본 자료를 레벨명 알파벳순으로 정렬하고, 각 레벨에 달린 코멘트를 함께 정리했습니다."
    )

    df = load_data()

    with st.sidebar:
        st.header("필터")
        search = st.text_input("레벨 이름 검색", "")
        only_with_comment = st.checkbox("코멘트가 있는 레벨만 보기", value=False)
        statuses = st.multiselect(
            "Status",
            options=sorted(df["Status"].unique()),
            default=sorted(df["Status"].unique()),
            format_func=lambda s: f"{s} ({STATUS_LABELS.get(s, s)})",
        )

    filtered = df[df["Status"].isin(statuses)]
    if search:
        filtered = filtered[filtered["Level"].str.contains(search, case=False, na=False)]
    if only_with_comment:
        filtered = filtered[filtered["Comment"].str.len() > 0]

    st.markdown(f"**총 {len(filtered)}개 레벨** (전체 {len(df)}개 중)")

    st.divider()

    # ------------------------------------------------------------
    # 레벨 목록: 알파벳순 + 코멘트 정리
    # ------------------------------------------------------------
    for _, row in filtered.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {row['Level']}")
                if row["Comment"]:
                    st.markdown(f"💬 **Comment:** {row['Comment']}")
                else:
                    st.markdown("💬 *Comment: 없음*")
            with col2:
                st.markdown(
                    f"**Rating:** {row['Rating']}  \n"
                    f"**Status:** {row['Status']} ({STATUS_LABELS.get(row['Status'], row['Status'])})  \n"
                    f"**ID:** {row['ID']}"
                )
            st.caption(
                f"FP 60: {row['60 FPS'] if pd.notna(row['60 FPS']) else '-'} | "
                f"120: {row['120 FPS'] if pd.notna(row['120 FPS']) else '-'} | "
                f"240: {row['240 FPS'] if pd.notna(row['240 FPS']) else '-'}"
            )
            st.divider()

    with st.expander("표(테이블) 형태로 보기"):
        st.dataframe(filtered.reset_index(drop=True), use_container_width=True)


if __name__ == "__main__":
    main()
