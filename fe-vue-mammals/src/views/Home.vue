<template>
  <div style="height: 100vh; background-color: #421983">
    <Navbar />
    <div v-if="loading" class="spinner-overlay">
      <div class="spinner"></div>
    </div>
    <div v-if="showResults" class="container">
      <div class="row mt-5 text-center">
        <h1 class="text-white">{{ predictedClass }}</h1>
      </div>
      <div class="row mt-3">
        <div class="text-white">
          <div v-if="details !== 'No details available'">
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Tinggi</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details['Height (cm)'] }} cm</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Berat</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details['Weight (kg)'] }} kg</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Warna</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details.Color }}</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Rentang Hidup</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details['Lifespan (years)'] }} years</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Jenis Makanan</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details.Diet }}</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Habitat</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details.Habitat }}</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Pemangsa</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details.Predators }}</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Kecepatan Rata-rata</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details['Average Speed (km/h)'] }} km/h</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Negara</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details['Countries Found'] }}</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Status Konservasi</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details['Conservation Status'] }}</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Family</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details.Family }}</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Periode Gestasi</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details['Gestation Period (days)'] }} days</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Kecepatan Tertinggi</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details['Top Speed (km/h)'] }} km/h</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Struktur Sosial</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details['Social Structure'] }}</h3>
              </div>
            </div>
            <div class="row text-center">
              <div class="col-5 text-end"><h3>Anak per Kelahiran</h3></div>
              <div class="col-7 text-start">
                <h3>: {{ details['Offspring per Birth'] }}</h3>
              </div>
            </div>
          </div>
          <div v-else>
            <div class="row text-center">
              <div class="col-12">
                <h3>Tidak ada informasi mengenai {{ predictedClass }}</h3>
              </div>
            </div>
          </div>
          <div class="wrap text-center mt-2">
            <button class="btn btn-secondary mt-3 text-" @click="resetForm">Back</button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="container text-center d-flex align-items-center">
      <div class="row mt-5">
        <div class="col-md-6 d-flex align-items-center">
          <div class="wrap">
            <h1 class="display-4 text-white">Mamalia apa Hayo?</h1>
            <p class="lead text-white">
              A quick website to identify what's mammal that you see today.
            </p>
            <form
              @submit.prevent="submitForm"
              class="d-flex justify-content-center align-items-center"
            >
              <input
                type="file"
                @change="handleFile"
                class="form-control me-2"
                aria-label="Upload File"
              />
              <button class="btn btn-success" type="submit">Cari</button>
            </form>
          </div>
        </div>
        <div class="col-md-6 d-flex align-items-center justify-content-center">
          <div class="my-5">
            <img src="@/assets/mammals.png" alt="Mammals" style="width: 100%" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import axios from 'axios'
const BASE_URL = import.meta.env.VITE_BASE_URL_API

export default {
  components: {
    Navbar
  },
  data() {
    return {
      file: null,
      loading: false,
      showResults: false,
      predictedClass: '',
      details: {}
    }
  },
  methods: {
    handleFile(event) {
      this.file = event.target.files[0]
    },
    async submitForm() {
      if (!this.file) {
        alert('Please select a file.')
        return
      }

      this.loading = true
      const formData = new FormData()
      formData.append('file', this.file)

      try {
        const response = await axios.post(BASE_URL + '/predict', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })

        this.predictedClass = response.data.predicted_class
        this.details = response.data.details
        this.showResults = true
      } catch (error) {
        console.error('Error uploading file:', error)
      } finally {
        this.loading = false
      }
    },
    resetForm() {
      this.file = null
      this.showResults = false
    }
  }
}
</script>
<style>
/* Form input styles */
form input {
  width: 250px;
}

form button {
  width: 100px;
}

/* Spinner styles */
.spinner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.spinner {
  border: 16px solid #f3f3f3;
  /* Light grey */
  border-top: 16px solid #3498db;
  /* Blue */
  border-radius: 50%;
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
