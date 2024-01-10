<template>
  <div class="h-screen bg-slate-900 flex flex-col">
    <div class="basis-1/3 flex flex-col items-center justify-center">
      <h1 class="text-white text-8xl text-center mt-4 font-extrabold ">Rythmly</h1>
    </div>
    <div class="basis-1/3">
      <ButtonsBPMComponent/>
    </div>
    <div class="basis-1/3 text-white text-center">
      <AIFeedbackComponent/>
    </div>
  </div> 
</template>

<script>
import ButtonsBPMComponent from './components/ButtonsBPMComponent.vue';
import AIFeedbackComponent from './components/AIFeedbackComponent.vue';

export default {
  name: 'App',
  components: {
    ButtonsBPMComponent,
    AIFeedbackComponent,
  }
}
</script>
