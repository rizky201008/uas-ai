<template>
  <div style="height: 100vh; background-color: #421983;">
    <Navbar />
    <div class="container text-center d-flex align-items-center">
      <div class="row mt-5">
        <div class="col-md-6 d-flex align-items-center">
          <div class="wrap">
            <h1 class="display-4 text-white">Mamalia apa Hayo?</h1>
            <p class="lead text-white">A quick website to identify what's mammal that you see today.
            </p>
            <form class="d-flex justify-content-center align-items-center">
              <input type="file" class="form-control me-2" placeholder="Insert email address" aria-label="Email">
              <button class="btn btn-success" type="submit">Cari</button>
            </form>
          </div>
        </div>
        <div class="col-md-6 d-flex align-items-center justify-content-center">
          <div class=" my-5">
            <img src="../assets/mammals.png" style="width: 100%;">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';

export default {
  components: {
    Navbar,
  },
};
</script>

<style>
form input {
  width: 250px;
}

form button {
  width: 100px;
}
</style>
