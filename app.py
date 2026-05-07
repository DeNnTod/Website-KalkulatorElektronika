from flask import Flask, render_template, request

app = Flask(__name__)

# ================= DATA =================
color_digit = {
    "hitam": 0, "coklat": 1, "merah": 2, "oranye": 3,
    "kuning": 4, "hijau": 5, "biru": 6, "ungu": 7,
    "abu-abu": 8, "putih": 9
}

multiplier = {
    "hitam": 1, "coklat": 10, "merah": 100, "oranye": 1000,
    "kuning": 10000, "hijau": 100000, "biru": 1000000,
    "ungu": 10000000, "abu-abu": 100000000, "putih": 1000000000,
    "emas": 0.1, "perak": 0.01
}

tolerance_res = {
    "coklat": "±1%", "merah": "±2%", "hijau": "±0.5%",
    "biru": "±0.25%", "ungu": "±0.1%", "abu-abu": "±0.05%",
    "emas": "±5%", "perak": "±10%"
}

tolerance_cap = {
    "J": "±5%", "K": "±10%", "M": "±20%", "Z": "+80%/-20%"
}

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("home.html")

# ===== RESISTOR =====
@app.route("/resistor", methods=["GET","POST"])
def resistor():
    hasil = None

    if request.method == "POST":
        mode = request.form.get("mode")

        b1 = request.form.get("band1")
        b2 = request.form.get("band2")
        b3 = request.form.get("band3")
        b4 = request.form.get("band4")
        b5 = request.form.get("band5")

        try:
            if mode == "4":
                nilai = (color_digit[b1]*10 + color_digit[b2]) * multiplier[b3]
                tol = tolerance_res.get(b4,"")
                hasil = f"{nilai} Ω {tol}"

            elif mode == "5":
                nilai = (color_digit[b1]*100 + color_digit[b2]*10 + color_digit[b3]) * multiplier[b4]
                tol = tolerance_res.get(b5,"")
                hasil = f"{nilai} Ω {tol}"

        except:
            hasil = "Input belum lengkap"

    return render_template("resistor.html",
        hasil=hasil,
        warna_digit=list(color_digit.keys()),
        warna_multiplier=list(multiplier.keys()),
        warna_tolerance=list(tolerance_res.keys())
    )

# ===== KAPASITOR =====
@app.route("/kapasitor", methods=["GET","POST"])
def kapasitor():
    hasil = None

    if request.method == "POST":
        kode = request.form.get("kode")
        tol = request.form.get("tol")

        if kode and kode.isdigit() and len(kode)==3:
            angka = int(kode[:2])
            pengali = int(kode[2])
            nilai_pf = angka*(10**pengali)

            if nilai_pf>=1_000_000:
                nilai = f"{nilai_pf/1_000_000} µF"
            elif nilai_pf>=1000:
                nilai = f"{nilai_pf/1000} nF"
            else:
                nilai = f"{nilai_pf} pF"

            hasil = f"{nilai} {tolerance_cap.get(tol,'')}"
        else:
            hasil = "Kode salah (contoh: 104)"

    return render_template("kapasitor.html",
        hasil=hasil,
        tol_list=tolerance_cap.keys()
    )

# ===== INDUKTOR =====
@app.route("/induktor", methods=["GET","POST"])
def induktor():
    hasil=None

    if request.method=="POST":
        b1=request.form.get("band1")
        b2=request.form.get("band2")
        b3=request.form.get("band3")

        if b1 and b2 and b3:
            nilai=(color_digit[b1]*10+color_digit[b2])*multiplier[b3]

            if nilai>=1_000_000:
                hasil=f"{nilai/1_000_000} H"
            elif nilai>=1000:
                hasil=f"{nilai/1000} mH"
            else:
                hasil=f"{nilai} µH"

    return render_template("induktor.html",
        hasil=hasil,
        warna_digit=list(color_digit.keys()),
        warna_multiplier=list(multiplier.keys())
    )

if __name__ == "__main__":
    app.run(debug=True)