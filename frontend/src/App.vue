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
import { analyzeSession, saveSession } from './api';

export default {
  name: 'App',
  data() {
    return {
      open: false,
      analysisMessage: "",
      analysisSuggestion: null, // "increase" | "decrease" | "maintain"
      feedback: false,
      scrolling: false,
      loading: false,
    }
  },
  components: {
    ButtonsBPMComponent,
    AIFeedbackComponent,
    Popup,
  },
  methods: {
    closePopup() {
      this.open = false;
      if (!this.feedback) {
        this.requestAnalysis();
      } else {
        this.$refs.aiComponent.aiListening();
      }
    },
    openPopup() {
      this.open = true;
    },
    feedbackEvent() {
      this.$refs.aiComponent.aiListening();
      const bpm = this.$refs.buttons.bpm;

      if (this.analysisSuggestion === 'increase') {
        this.increaseTheBPM();
      } else if (this.analysisSuggestion === 'decrease') {
        this.decreaseTheBPM();
      }

      saveSession({
        bpm,
        duration_seconds: 5,
        success: this.analysisSuggestion === 'increase',
      });

      this.open = false;
      this.scrolling = false;
    },
    aiTrigger() {
      this.showRecordingMessage();
    },
    showRecordingMessage() {
      this.feedback = false;
      this.analysisMessage = "The recording was done successfully. Please wait for the AI Assistant to finish analyzing...";
      this.openPopup();
    },
    async requestAnalysis() {
      this.loading = true;
      const bpm = this.$refs.buttons.bpm;

      try {
        const result = await analyzeSession(bpm);
        this.analysisMessage = result.message;
        this.analysisSuggestion = result.suggestion;
        this.feedback = true;
        this.openPopup();
      } catch {
        this.analysisMessage = "Could not reach the AI server. Please make sure the backend is running.";
        this.analysisSuggestion = null;
        this.feedback = false;
        this.openPopup();
      } finally {
        this.loading = false;
      }
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
      this.scrolling = true;
    },
  },

  computed: {
    changeOpacity() {
      return {
        opacity: this.open ? 0.5 : 1,
      }
    },
    message() {
      return this.analysisMessage;
    },
  },
}
</script>
