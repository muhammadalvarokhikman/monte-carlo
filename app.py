import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    # Setup halaman utama
    st.set_page_config(page_title="Simulasi Monte Carlo", layout="wide")

    # Sidebar dengan logo dan informasi "Created by"
    st.sidebar.image(
        "logo.png", caption="Universitas Muhammadiyah Semarang", use_container_width=True
    )
    st.sidebar.title("Navigasi")
    menu = ["Data Mahasiswa Baru", "Monte Carlo"]
    choice = st.sidebar.selectbox("Pilih Menu", menu)

    # Tambahkan informasi "Created by" di bawah navigasi
    st.sidebar.markdown(
        """
        ---
        **✏️ Created By**  
        **Nama**: Muhammad Alvaro Khikman  
        **NIM**: B2A022061
        """
    )

    # Header aplikasi
    st.markdown(
        """
        <div style="background-color:#0d6efd;padding:15px;border-radius:5px;margin-bottom:20px;text-align:center;">
            <h1 style="color:white;">Aplikasi Simulasi Monte Carlo</h1>
            <h3 style="color:white;">Analisis Data Mahasiswa Baru</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if choice == "Data Mahasiswa Baru":
        # Data awal
        data_mahasiswa = pd.DataFrame(
            {
                "Tahun": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
                "Jumlah Pendaftar": [1383, 2293, 2634, 2707, 2734, 2872, 3396, 3700, 3715, 4670],
            }
        )

        # Tampilkan tabel
        st.subheader("Data Mahasiswa Baru")
        st.dataframe(data_mahasiswa)

        # Tambahkan grafik visualisasi
        st.subheader("Visualisasi Data")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="Tahun", y="Jumlah Pendaftar", data=data_mahasiswa, palette="viridis", ax=ax)
        ax.set_title("Jumlah Pendaftar Per Tahun", fontsize=16)
        ax.set_xlabel("Tahun")
        ax.set_ylabel("Jumlah Pendaftar")
        st.pyplot(fig)

    elif choice == "Monte Carlo":
        # Data awal
        data = pd.DataFrame(
            {
                "Tahun": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
                "Jumlah Pendaftar": [1383, 2293, 2634, 2707, 2734, 2872, 3396, 3700, 3715, 4670],
            }
        )

        # Hitung probabilitas, kumulatif, dan interval
        total_pendaftar = data["Jumlah Pendaftar"].sum()
        data["Probabilitas"] = data["Jumlah Pendaftar"] / total_pendaftar
        data["Kumulatif"] = data["Probabilitas"].cumsum()

        def calculate_interval(cumulative, probability):
            start = int((cumulative - probability) * 1000)
            end = int(cumulative * 1000) - 1
            return f"{start}-{end}"

        data["Interval"] = data.apply(
            lambda row: calculate_interval(row["Kumulatif"], row["Probabilitas"]), axis=1
        )

        # Tambahkan kolom "No" untuk nomor urut
        data.reset_index(inplace=True)
        data.rename(columns={"index": "No"}, inplace=True)
        data["No"] += 1

        # Format tabel
        data = data[["No", "Tahun", "Jumlah Pendaftar", "Probabilitas", "Kumulatif", "Interval"]]

        # Tampilkan tabel probabilitas dan interval
        st.subheader("Hitung Interval Probabilitas")
        st.dataframe(data)

        # Grafik probabilitas
        st.subheader("Visualisasi Probabilitas")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="Tahun", y="Probabilitas", data=data, palette="coolwarm", ax=ax)
        ax.set_title("Probabilitas Pendaftar Per Tahun", fontsize=16)
        ax.set_xlabel("Tahun")
        ax.set_ylabel("Probabilitas")
        st.pyplot(fig)

        # Simulasi Monte Carlo
        # Parameter generator
        a = 25
        c = 15
        m = 99
        z0 = 50

        # Jumlah simulasi
        n = st.slider("Jumlah Simulasi", min_value=1, max_value=20, value=5)

        # Generate bilangan acak dan buat tabel
        zi = [z0]
        az_plus_c = []
        mod_m = []
        angka_tiga_digit = []
        predictions = []

        for _ in range(n):
            z_next = (a * zi[-1] + c)
            mod = z_next % m
            three_digit = int((mod / m) * 1000)

            # Cari prediksi berdasarkan interval
            prediksi = None
            for _, row in data.iterrows():
                batas = list(map(int, row["Interval"].split("-")))
                if batas[0] <= three_digit <= batas[1]:
                    prediksi = row["Jumlah Pendaftar"]
                    break

            # Simpan hasil
            az_plus_c.append(z_next)
            mod_m.append(mod)
            angka_tiga_digit.append(three_digit)
            predictions.append(prediksi)

            zi.append(mod)

        # Buat DataFrame hasil
        hasil = pd.DataFrame(
            {
                "Zi": zi[:-1],
                "(aZi) + C": az_plus_c,
                "(aZi) + C mod m": mod_m,
                "Angka tiga digit": angka_tiga_digit,
                "Prediksi": predictions,
            }
        )

        # Tampilkan hasil simulasi
        st.subheader("Hasil Simulasi Monte Carlo")
        st.dataframe(hasil)

        # Grafik hasil simulasi
        st.subheader("Visualisasi Hasil Simulasi")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x=range(1, n + 1), y=predictions, marker="o", ax=ax, color="green")
        ax.set_title("Prediksi Monte Carlo", fontsize=16)
        ax.set_xlabel("Iterasi")
        ax.set_ylabel("Jumlah Pendaftar")
        st.pyplot(fig)

        # Prediksi tahun berikutnya
        st.write(f"Prediksi jumlah pendaftar tahun berikutnya: **{predictions[-1]}**")


if __name__ == "__main__":
    main()
