<template>
  <div class="metronome">
    <div class="bpm-display">{{ bpm }} BPM</div>
    <button @click="decreaseBPM">-</button>
    <button @click="increaseBPM">+</button>
    <button @click="startStopMetronome">{{ metronomeRunning ? 'Stop' : 'Start' }}</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bpm: 120, // Initial BPM
      metronomeRunning: false,
      audioContext: null,
      clickOscillator: null,
      woodblockOscillator: null,
      gainNode: null,
      woodblockGainNode: null,
    };
  },
  methods: {
    startStopMetronome() {
      if (this.metronomeRunning) {
        this.stopMetronome();
      } else {
        this.startMetronome();
      }
    },
    startMetronome() {
      this.metronomeRunning = true;

      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      this.clickOscillator = this.createOscillator('triangle', 1000); // Click sound
      this.woodblockOscillator = this.createOscillator('square', 1200); // Woodblock-like sound
      this.gainNode = this.createGainNode();
      this.woodblockGainNode = this.createGainNode();

      this.clickOscillator.connect(this.gainNode);
      this.woodblockOscillator.connect(this.woodblockGainNode);
      this.gainNode.connect(this.audioContext.destination);
      this.woodblockGainNode.connect(this.audioContext.destination);

      this.clickOscillator.start();
      this.woodblockOscillator.start();

      this.scheduleTick();
    },

    stopMetronome() {
      this.metronomeRunning = false;

      if (this.clickOscillator) {
        this.clickOscillator.stop();
        this.clickOscillator.disconnect();
      }

      if (this.woodblockOscillator) {
        this.woodblockOscillator.stop();
        this.woodblockOscillator.disconnect();
      }

      if (this.gainNode) {
        this.gainNode.disconnect();
      }

      if (this.woodblockGainNode) {
        this.woodblockGainNode.disconnect();
      }

      if (this.audioContext) {
        this.audioContext.close();
      }
    },
    scheduleTick() {
      const interval = (60/ this.bpm);
      const startTime = this.audioContext.currentTime;
      let nextTickTime = startTime;

      const tick = () => {
        if (!this.metronomeRunning) return;

        this.playTickSound();

        nextTickTime += interval;
        setTimeout(tick, nextTickTime * 1000 - this.audioContext.currentTime * 1000);
      };

      tick();
    },
    playTickSound() {
      this.clickOscillator.frequency.setValueAtTime(1000, this.audioContext.currentTime);
      this.gainNode.gain.setValueAtTime(0.5, this.audioContext.currentTime);

      this.woodblockOscillator.frequency.setValueAtTime(800, this.audioContext.currentTime);
      this.woodblockGainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);

      // Accent every 4th beat with a louder woodblock-like sound
      // TODO has to be changed
      if (this.audioContext.currentTime % (60 / this.bpm * 4) < 0.05) {
        this.woodblockGainNode.gain.setValueAtTime(1, this.audioContext.currentTime);
      }

      // Ramp down the volume
      const releaseTime = 0.05; // seconds
      this.gainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + releaseTime);
      this.woodblockGainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + releaseTime);
    },
    createOscillator(type, frequency) {
      const oscillator = this.audioContext.createOscillator();
      oscillator.type = type;
      oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
      return oscillator;
    },
    createGainNode() {
      return this.audioContext.createGain();
    },
    increaseBPM() {
      this.bpm += 5;
    },

    decreaseBPM() {
      this.bpm -= 5
    },
  },
};
</script>

<style scoped>
.metronome {
  text-align: center;
  margin: 20px;
}

.bpm-display {
  font-size: 20px;
  margin-bottom: 10px;
}

button {
  font-size: 16px;
  margin: 5px;
  padding: 5px 10px;
  cursor: pointer;
}
</style>
