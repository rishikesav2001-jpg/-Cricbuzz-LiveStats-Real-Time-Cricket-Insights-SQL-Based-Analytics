import streamlit as st
import pandas as pd
from utils.db_connection import get_connection

def show():

    st.title("🛠 All Players CRUD")

    conn = get_connection()

    if not conn:
        st.error("Database connection failed")
        return

    # ==========================
    # READ DATA
    # ==========================

    query = """
    SELECT
        playerId,
        playerName,
        role,
        battingStyle,
        bowlingStyle
    FROM all_players
    """

    df = pd.read_sql(query, conn)

    st.subheader("📋 Players Table")

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic"
    )

    # ==========================
    # SAVE CHANGES
    # ==========================

    if st.button("💾 Save Changes"):

        cur = conn.cursor()

        try:

            for _, row in edited_df.iterrows():

                cur.execute(
                    """
                    UPDATE all_players
                    SET
                        playerName=%s,
                        role=%s,
                        battingStyle=%s,
                        bowlingStyle=%s
                    WHERE playerId=%s
                    """,
                    (
                        row["playerName"],
                        row["role"],
                        row["battingStyle"],
                        row["bowlingStyle"],
                        row["playerId"]
                    )
                )

            conn.commit()

            st.success("✅ All changes saved successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

        finally:
            cur.close()

    # ==========================
    # ADD NEW PLAYER
    # ==========================

    st.markdown("---")
    st.subheader("➕ Add New Player")

    player_id = st.number_input(
        "Player ID",
        min_value=1,
        step=1
    )

    player_name = st.text_input("Player Name")

    role = st.text_input("Role")

    batting_style = st.text_input("Batting Style")

    bowling_style = st.text_input("Bowling Style")

    if st.button("Add Player"):

        cur = conn.cursor()

        try:

            cur.execute(
                """
                INSERT INTO all_players
                (
                    playerId,
                    playerName,
                    role,
                    battingStyle,
                    bowlingStyle
                )
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    player_id,
                    player_name,
                    role,
                    batting_style,
                    bowling_style
                )
            )

            conn.commit()

            st.success("✅ Player added successfully!")

        except Exception as e:

            st.error(f"Error: {e}")

        finally:

            cur.close()
    # ==========================
    # UPDATE PLAYER
    # ==========================

    st.markdown("---")
    st.subheader("✏️ Update Player")

    player_ids = df["playerId"].tolist()

    selected_id = st.selectbox(
        "Select Player",
        player_ids,
        key="update_player"
    )

    selected_row = df[df["playerId"] == selected_id].iloc[0]

    update_name = st.text_input(
        "Player Name",
        value=selected_row["playerName"]
    )

    update_role = st.text_input(
        "Role",
        value=selected_row["role"]
    )

    update_batting = st.text_input(
        "Batting Style",
        value=selected_row["battingStyle"]
    )

    update_bowling = st.text_input(
        "Bowling Style",
        value=selected_row["bowlingStyle"]
    )

    if st.button("Update Player"):

        cur = conn.cursor()

        try:

            cur.execute(
                """
             UPDATE all_players
             SET
                    playerName=%s,
                    role=%s,
                    battingStyle=%s,
                    bowlingStyle=%s
                WHERE playerId=%s
                """,
                (
                    update_name,
                    update_role,
                    update_batting,
                    update_bowling,
                    selected_id
                )
            )

            conn.commit()

            st.success("✅ Player Updated Successfully")

        except Exception as e:

            st.error(f"Error: {e}")

        finally:

            cur.close()
    # ==========================
    # DELETE PLAYER
    # ==========================

    st.markdown("---")
    st.subheader("🗑 Delete Player")

    player_ids = df["playerId"].tolist()

    selected_player = st.selectbox(
        "Select Player ID",
        player_ids
    )

    if st.button("Delete Player"):

        cur = conn.cursor()

        try:

            cur.execute(
                """
                DELETE FROM all_players
                WHERE playerId=%s
                """,
                (selected_player,)
            )

            conn.commit()

            st.success("✅ Player deleted successfully!")

        except Exception as e:

            st.error(f"Error: {e}")

        finally:

            cur.close()

    conn.close()