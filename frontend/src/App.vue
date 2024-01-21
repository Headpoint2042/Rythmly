<template>
  <div class="h-screen bg-slate-900 flex flex-col" :style="changeOpacity"  @wheel="handleMouseWheel">
    <div class="basis-1/3 flex flex-col items-center justify-center">
      <h1 class="text-white text-8xl text-center mt-4 font-extrabold">Rythmly</h1>
    </div>
    <div class="basis-1/3">
      <ButtonsBPMComponent ref="buttons"/>
    </div>
    <div class="basis-1/3 text-white text-center">
      <AIFeedbackComponent @ailistening="aiTrigger" ref="aiComponent"/>
    </div>
    <teleport to="#popup">
      <div v-if="open">
        <Popup @close="closePopup" @feedback="feedbackEvent" :message="message" :feedback="feedback" :scrolling="scrolling"/>
      </div>
    </teleport>
  </div> 
</template>

<script>
import ButtonsBPMComponent from './components/ButtonsBPMComponent.vue';
import AIFeedbackComponent from './components/AIFeedbackComponent.vue';
import Popup from './components/PopupComponent.vue';

export default {
  name: 'App',
  data() {
    return {
      open: false,
      msg1: "The recording was done successfully. Please wait for the AI Assistant to finish analyzing",
      msg2: "Unfortunately, your playing was not done properly. It would be recommended to try to practice with 10 BPM slower",
      msg3: "Congratulations, your playing seems to be done properly. I would advice to increase the BPM with 10",
      feedback: false,
      scrolling: false, // Added scrolling boolean
    }
  },
  components: {
    ButtonsBPMComponent,
    AIFeedbackComponent,
    Popup,
  },
  methods: {
    closePopup() {
      this.open = false
      if (!this.feedback) {
        this.startDelayedEvent(true);
      } else {
        this.$refs.aiComponent.aiListening();
      }
    },
    openPopup() {
      this.open = true
    },
    feedbackEvent(param1) {
      this.$refs.aiComponent.aiListening();
      if (param1) {
        this.increaseTheBPM();
      } else {
        this.decreaseTheBPM();
      }
      this.open = false;
      this.scrolling = false;
    },
    aiTrigger() {
      this.startDelayedEvent()
    },
    startDelayedEvent(feedback = false) {
      setTimeout(() => {
        this.feedback = feedback
        this.openPopup()
      }, 5000);
    },
    decreaseTheBPM() {
      this.$refs.buttons.decreaseBPM();
      this.$refs.buttons.decreaseBPM();
    },
    increaseTheBPM() {
      this.$refs.buttons.increaseBPM();
      this.$refs.buttons.increaseBPM();
    },
    handleMouseWheel() {
      this.scrolling = true; // Set scrolling to true when the mouse wheel is triggered
    },
  },

  computed: {
    changeOpacity() {
      return {
        opacity: this.open ? 0.5 : 1,
      }
    },
    message() {
      if (this.feedback) {
        return this.scrolling ? this.msg3 : this.msg2;
      } else {
        return this.msg1;
      }
    },
  },
}
</script>
