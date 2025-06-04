<!---
Vii25-hub/Vii25-hub is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nama = $_POST['nama'];
    $nomor = $_POST['nomor'];
    $kelas = $_POST['kelas'];
    $catatan = $_POST['catatan'];

    $to = "privatkursusonline@gmail.com"; // ganti dengan emailmu
    $subject = "Pendaftaran Kursus";
    $message = "Nama: $nama\nNo. WhatsApp: $nomor\nKelas: $kelas\nCatatan: $catatan";
    $headers = "From: noreply@domainmu.com";

    if (mail($to, $subject, $message, $headers)) {
        $status = "Berhasil dikirim!";
    } else {
        $status = "Gagal mengirim. Coba lagi.";
    }
}
?>
<!DOCTYPE html><html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kursus Privat Online</title>
  <style>
    body {
      margin: 0;
      font-family: 'Poppins', sans-serif;
      background-color: #f9f9f9;
      color: #333;
    }
    header {
      background-color: #1e88e5;
      color: white;
      padding: 1rem 2rem;
      position: sticky;
      top: 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      z-index: 1000;
    }
    nav a {
      color: white;
      text-decoration: none;
      margin-left: 1.5rem;
      font-weight: 500;
    }
    .hero {
      padding: 3rem 2rem;
      background-color: #e3f2fd;
      text-align: center;
    }
    .hero h1 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
    }
    .hero p {
      font-size: 1.2rem;
      margin-bottom: 2rem;
    }
    .button {
      padding: 0.8rem 1.5rem;
      background-color: #1e88e5;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      cursor: pointer;
    }
    .courses {
      padding: 2rem;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
    }
    .course-card {
      background: white;
      padding: 1.5rem;
      border-radius: 12px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.05);
      cursor: pointer;
    }
    .course-card h3 {
      margin-top: 0;
      color: #1e88e5;
    }
    .course-detail {
      display: none;
      background: #fff;
      padding: 1rem 2rem;
      margin: 0 2rem 2rem 2rem;
      border-left: 4px solid #1e88e5;
    }
    .form-section {
      padding: 2rem;
      background-color: #fff;
    }
    .form-section h2 {
      text-align: center;
      margin-bottom: 1.5rem;
    }
    form {
      max-width: 500px;
      margin: auto;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    input, select, textarea {
      padding: 0.8rem;
      font-size: 1rem;
      border: 1px solid #ccc;
      border-radius: 8px;
    }
    footer {
      background-color: #1e88e5;
      color: white;
      text-align: center;
      padding: 1rem;
      margin-top: 2rem;
    }
  </style>
  <script>
    function toggleDetail(id) {
      const detail = document.getElementById(id);
      detail.style.display = detail.style.display === 'block' ? 'none' : 'block';
    }
  </script>
</head>
<body>
  <header>
    <div><strong>Kursus Privat</strong></div>
    <nav>
      <a href="#home">Beranda</a>
      <a href="#courses">Kelas</a>
      <a href="#form">Daftar</a>
      <a href="#contact">Kontak</a>
    </nav>
  </header>  <section class="hero" id="home">
    <h1>Belajar Coding & Statistik Terapan Jadi Mudah</h1>
    <p>Kursus daring dengan harga terjangkau mulai Rp25k/jam</p>
    <button class="button" onclick="location.href='#courses'">Lihat Kelas</button>
  </section>  <section class="courses" id="courses">
    <div class="course-card" onclick="toggleDetail('python')">
      <h3>Python Dasar</h3>
      <p>Klik untuk lihat detail materi</p>
    </div>
    <div id="python" class="course-detail">
      <p>Kursus ini membahas konsep dasar pemrograman, sintaks Python, tipe data, struktur kontrol, fungsi, dan praktik membuat program sederhana. Materi meliputi operator, percabangan, perulangan, serta studi kasus mini untuk latihan.</p>
    </div><div class="course-card" onclick="toggleDetail('c')">
  <h3>Bahasa C Dasar</h3>
  <p>Klik untuk lihat detail materi</p>
</div>
<div id="c" class="course-detail">
  <p>Kursus ini membahas dasar-dasar bahasa C termasuk struktur program, tipe data, pointer, percabangan, perulangan, serta fungsi. Disertai praktik membuat program sederhana dan latihan studi kasus.</p>
</div>

<div class="course-card" onclick="toggleDetail('sql')">
  <h3>SQL & Query Database</h3>
  <p>Klik untuk lihat detail materi</p>
</div>
<div id="sql" class="course-detail">
  <p>Kursus ini mengajarkan dasar-dasar SQL untuk membuat, membaca, memperbarui, dan menghapus data di database relasional. Materi meliputi SELECT, INSERT, UPDATE, DELETE, JOIN antar tabel, dan studi kasus praktik pada sample database.</p>
</div>

<div class="course-card" onclick="toggleDetail('spss')">
  <h3>Statistika Terapan (SPSS)</h3>
  <p>Klik untuk lihat detail materi</p>
</div>
<div id="spss" class="course-detail">
  <p>Kursus ini membahas konsep dasar statistika terapan, teknik analisis data, dan penggunaan SPSS untuk pengolahan data statistik. Materi meliputi uji hipotesis, one sample t-test, two sample t-test, serta uji-uji statistik lain yang umum digunakan dalam penelitian.</p>
</div>

  </section>  <section class="form-section" id="form">
    <h2>Formulir Pendaftaran</h2>
    <form>
      <input type="text" placeholder="Nama Lengkap" required>
      <input type="tel" placeholder="Nomor WhatsApp" required>
      <select required>
        <option value="">Pilih Kelas</option>
        <option>Python Dasar</option>
        <option>Bahasa C Dasar</option>
        <option>SQL & Query Database</option>
        <option>Statistika Terapan (SPSS)</option>
      </select>
      <textarea placeholder="Catatan tambahan (opsional)"></textarea>
      <button type="submit" class="button">Kirim</button>
    </form>
    <?php if (isset($status)) echo \"<p>$status</p>\"; ?>
  </section>  <footer id="contact">
    <p>Hubungi via WhatsApp: 0881025159813 | Email: privatkursusonline@email.com</p>
    <p>&copy; 2025 Kursus Privat Online</p>
  </footer>
</body>
</html>
