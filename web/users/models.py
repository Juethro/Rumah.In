from django.db import models

# Create your models here.
class AutoLog(models.Model):
    log = models.CharField(max_length=200)
    date = models.DateTimeField()
    
class Properti(models.Model):
    judul = models.CharField(max_length=255, null=True, blank=True)
    harga = models.CharField(max_length=100, null=True, blank=True)
    cicilan = models.CharField(max_length=100, null=True, blank=True)
    kecamatan = models.CharField(max_length=255, null=True, blank=True)
    luas_tanah_front = models.CharField(max_length=100, null=True, blank=True)
    luas_bangunan_front = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    fasilitas = models.TextField(null=True, blank=True)
    last_update = models.CharField(max_length=100, null=True, blank=True)
    kamar_tidur = models.FloatField(null=True, blank=True)
    kamar_mandi = models.FloatField(null=True, blank=True)
    luas_tanah = models.CharField(max_length=100, null=True, blank=True)
    luas_bangunan = models.CharField(max_length=100, null=True, blank=True)
    carport = models.FloatField(null=True, blank=True)
    tipe_properti = models.CharField(max_length=255, null=True, blank=True)
    sertifikat = models.CharField(max_length=100, null=True, blank=True)
    kamar_pembantu = models.FloatField(null=True, blank=True)
    kamar_mandi_pembantu = models.FloatField(null=True, blank=True)
    dapur = models.FloatField(null=True, blank=True)
    ruang_makan = models.CharField(max_length=255, null=True, blank=True)
    ruang_tamu = models.CharField(max_length=255, null=True, blank=True)
    kondisi_perabotan = models.CharField(max_length=255, null=True, blank=True)
    material_bangunan = models.CharField(max_length=255, null=True, blank=True)
    material_lantai = models.CharField(max_length=255, null=True, blank=True)
    jumlah_lantai = models.FloatField(null=True, blank=True)
    hadap = models.CharField(max_length=100, null=True, blank=True)
    konsep_dan_gaya_rumah = models.CharField(max_length=255, null=True, blank=True)
    pemandangan = models.CharField(max_length=255, null=True, blank=True)
    terjangkau_internet = models.CharField(max_length=255, null=True, blank=True)
    lebar_jalan = models.CharField(max_length=100, null=True, blank=True)
    tahun_dibangun = models.FloatField(null=True, blank=True)
    tahun_di_renovasi = models.FloatField(null=True, blank=True)
    sumber_air = models.CharField(max_length=100, null=True, blank=True)
    hook = models.CharField(max_length=100, null=True, blank=True)
    kondisi_properti = models.CharField(max_length=255, null=True, blank=True)
    tipe_iklan = models.CharField(max_length=100, null=True, blank=True)
    id_iklan = models.CharField(max_length=100, null=True, blank=True)
    deskripsi = models.TextField(null=True, blank=True)
    daya_listrik = models.CharField(max_length=100, null=True, blank=True)
    garasi = models.FloatField(null=True, blank=True)
    nomor_lantai = models.FloatField(null=True, blank=True)

class ModelRegresi(models.Model):
    waktu = models.DateField()
    versi = models.CharField(max_length=100)
    path = models.CharField(max_length=500)

class Training(models.Model):
    judul = models.TextField(max_length=255)
    harga = models.FloatField(max_length=100)
    kecamatan = models.IntegerField()
    link = models.TextField(max_length=20)
    images_link = models.TextField(max_length=100)
    kamar_tidur = models.FloatField(max_length=100)
    kamar_mandi = models.FloatField(max_length=100)
    luas_tanah = models.FloatField(max_length=100)
    luas_bangunan = models.FloatField(max_length=100)
    carport = models.FloatField(max_length=100)
    sertifikat = models.IntegerField()
    daya_listrik = models.FloatField(max_length=100)
    kamar_pembantu = models.FloatField(max_length=100)
    kamar_mandi_pembantu = models.FloatField(max_length=100)
    dapur = models.FloatField(max_length=100)
    ruang_makan = models.IntegerField()
    ruang_tamu = models.IntegerField()
    kondisi_perabotan = models.IntegerField()
    jumlah_lantai = models.FloatField(max_length=100)
    hadap = models.IntegerField()
    konsep_dan_gaya_rumah = models.IntegerField()
    pemandangan = models.IntegerField()
    terjangkau_internet = models.IntegerField()
    lebar_jalan = models.FloatField(max_length=100)
    tahun_dibangun = models.FloatField(max_length=100)
    tahun_di_renovasi = models.FloatField(max_length=100)
    sumber_air = models.IntegerField()
    hook = models.IntegerField()
    kondisi_properti = models.IntegerField()
    garasi = models.IntegerField()
    distance_gerbangtol = models.FloatField(max_length=100)
    distance_school = models.FloatField(max_length=100)
    distance_hospital = models.FloatField(max_length=100)
    distance_tokoobat = models.FloatField(max_length=100)
    bata_hebel = models.IntegerField(default=0)
    bata_merah = models.IntegerField(default=0)
    batako = models.IntegerField(default=0)
    beton = models.IntegerField(default=0)
    granit = models.IntegerField(default=0)
    keramik = models.IntegerField(default=0)
    marmer = models.IntegerField(default=0)
    ubin = models.IntegerField(default=0)
    vinyl = models.IntegerField(default=0)
    ac = models.IntegerField(default=0)
    akses_parkir = models.IntegerField(default=0)
    balcony = models.IntegerField(default=0)
    built_in_robes = models.IntegerField(default=0)
    cctv = models.IntegerField(default=0)
    golf_view = models.IntegerField(default=0)
    jalur_telepon = models.IntegerField(default=0)
    jogging_track = models.IntegerField(default=0)
    keamanan = models.IntegerField(default=0)
    kitchen_set = models.IntegerField(default=0)
    kolam_ikan = models.IntegerField(default=0)
    kolam_renang = models.IntegerField(default=0)
    lapangan_basket = models.IntegerField(default=0)
    lapangan_bola = models.IntegerField(default=0)
    lapangan_bulu_tangkis = models.IntegerField(default=0)
    lapangan_tenis = models.IntegerField(default=0)
    lapangan_voli = models.IntegerField(default=0)
    masjid = models.IntegerField(default=0)
    one_gate_system = models.IntegerField(default=0)
    pemanas_air = models.IntegerField(default=0)
    separate_dining_room = models.IntegerField(default=0)
    taman = models.IntegerField(default=0)
    tempat_gym = models.IntegerField(default=0)
    tempat_jemuran = models.IntegerField(default=0)
    tempat_laundry = models.IntegerField(default=0)
    wastafel = models.IntegerField(default=0)
    kecamatan_1 = models.CharField(max_length=255)
    latitude = models.FloatField(max_length=100)
    longitude = models.FloatField(max_length=100)
    label = models.IntegerField()

class UserInput(models.Model):
    judul = models.TextField(max_length=255)
    harga = models.FloatField(max_length=100)
    kecamatan = models.IntegerField()
    link = models.TextField(max_length=20)
    images_link = models.TextField(max_length=20)
    kamar_tidur = models.FloatField(max_length=100)
    kamar_mandi = models.FloatField(max_length=100)
    luas_tanah = models.FloatField(max_length=100)
    luas_bangunan = models.FloatField(max_length=100)
    carport = models.FloatField(max_length=100)
    sertifikat = models.IntegerField()
    daya_listrik = models.FloatField(max_length=100)
    kamar_pembantu = models.FloatField(max_length=100)
    kamar_mandi_pembantu = models.FloatField(max_length=100)
    dapur = models.FloatField(max_length=100)
    ruang_makan = models.IntegerField()
    ruang_tamu = models.IntegerField()
    kondisi_perabotan = models.IntegerField()
    jumlah_lantai = models.FloatField(max_length=100)
    hadap = models.IntegerField()
    konsep_dan_gaya_rumah = models.IntegerField()
    pemandangan = models.IntegerField()
    terjangkau_internet = models.IntegerField()
    lebar_jalan = models.FloatField(max_length=100)
    tahun_dibangun = models.FloatField(max_length=100)
    tahun_di_renovasi = models.FloatField(max_length=100)
    sumber_air = models.IntegerField()
    hook = models.IntegerField()
    kondisi_properti = models.IntegerField()
    garasi = models.IntegerField()
    distance_gerbangtol = models.FloatField(max_length=100)
    distance_school = models.FloatField(max_length=100)
    distance_hospital = models.FloatField(max_length=100)
    distance_tokoobat = models.FloatField(max_length=100)
    bata_hebel = models.IntegerField(default=0)
    bata_merah = models.IntegerField(default=0)
    batako = models.IntegerField(default=0)
    beton = models.IntegerField(default=0)
    granit = models.IntegerField(default=0)
    keramik = models.IntegerField(default=0)
    marmer = models.IntegerField(default=0)
    ubin = models.IntegerField(default=0)
    vinyl = models.IntegerField(default=0)
    ac = models.IntegerField(default=0)
    akses_parkir = models.IntegerField(default=0)
    balcony = models.IntegerField(default=0)
    built_in_robes = models.IntegerField(default=0)
    cctv = models.IntegerField(default=0)
    golf_view = models.IntegerField(default=0)
    jalur_telepon = models.IntegerField(default=0)
    jogging_track = models.IntegerField(default=0)
    keamanan = models.IntegerField(default=0)
    kitchen_set = models.IntegerField(default=0)
    kolam_ikan = models.IntegerField(default=0)
    kolam_renang = models.IntegerField(default=0)
    lapangan_basket = models.IntegerField(default=0)
    lapangan_bola = models.IntegerField(default=0)
    lapangan_bulu_tangkis = models.IntegerField(default=0)
    lapangan_tenis = models.IntegerField(default=0)
    lapangan_voli = models.IntegerField(default=0)
    masjid = models.IntegerField(default=0)
    one_gate_system = models.IntegerField(default=0)
    pemanas_air = models.IntegerField(default=0)
    separate_dining_room = models.IntegerField(default=0)
    taman = models.IntegerField(default=0)
    tempat_gym = models.IntegerField(default=0)
    tempat_jemuran = models.IntegerField(default=0)
    tempat_laundry = models.IntegerField(default=0)
    wastafel = models.IntegerField(default=0)
    kecamatan_1 = models.CharField(max_length=255)
    latitude = models.FloatField(max_length=100)
    longitude = models.FloatField(max_length=100)
    label = models.IntegerField()
    