<template>
  <div class="flex flex-col">
    <div class="flex justify-center mb-4 basis-1/3 h-full">
      <div v-for="(light, index) in lights" :key="index" :class="{ 'bg-yellow-500': light === 'woodblock', 'bg-gray-400': light !== 'woodblock', 'w-12 h-12 rounded-full m-8': true }"></div>
    </div>
    <div class="text-white flex flex-row justify-center font-bold basis-1/3 h-full">
      <button class="text-6xl border-2 m-10 size-24" @click="decreaseBPM">-5</button>
      <div class="text-5xl underline border-white flex items-center">{{ bpm }} BPM</div>
      <button class="text-6xl border-2 m-10 size-24" @click="increaseBPM">+5</button>
    </div>
    <div class="flex justify-center basis-1/3">
      <button @click="startStopMetronome" :class="{ 'border-green-500 text-green-500': !metronomeRunning, 'border-red-500 text-red-500': metronomeRunning }" class="text-3xl w-24 h-24 rounded-full cursor-pointer flex items-center justify-center border-8 h-full">
      <span v-if="!metronomeRunning">&#9658;</span>
      <span v-else>■</span>
    </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bpm: 120,
      metronomeRunning: false,
      audioContext: null,
      clickOscillator: null,
      woodblockOscillator: null,
      gainNode: null,
      woodblockGainNode: null,
      lights: ['', '', '', ''],
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
      this.clickOscillator = this.createOscillator('triangle', 1000);
      this.woodblockOscillator = this.createOscillator('square', 1200);
      this.gainNode = this.createGainNode();
      this.woodblockGainNode = this.createGainNode();
      this.clickOscillator.connect(this.gainNode);
      this.woodblockOscillator.connect(this.woodblockGainNode);
      this.gainNode.connect(this.audioContext.destination);
      this.woodblockGainNode.connect(this.audioContext.destination);
      this.clickOscillator.start();
      this.woodblockOscillator.start();
      this.scheduleTick();

      // Initialize the lights to indicate the first light as active
      this.lights = ['woodblock', '', '', ''];
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
      const interval = (60 / this.bpm) * 1000;
      let lightIndex = 0;

      const tick = () => {
        if (!this.metronomeRunning) return;
        
        this.lights = ['', '', '', ''];
        this.lights[lightIndex] = 'woodblock';

        this.playTickSound();

        lightIndex = (lightIndex + 1) % 4; // Update the light index for the next tick
        setTimeout(tick, interval);
      };

      tick();
    },


    playTickSound() {
      this.clickOscillator.frequency.setValueAtTime(1000, this.audioContext.currentTime);
      this.gainNode.gain.setValueAtTime(0.5, this.audioContext.currentTime);
      this.woodblockOscillator.frequency.setValueAtTime(1200, this.audioContext.currentTime);
      this.woodblockGainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);

      const isAccentedBeat = this.audioContext.currentTime % (60 / this.bpm * 4) < 0.05;

      if (isAccentedBeat) {
        this.woodblockGainNode.gain.setValueAtTime(1, this.audioContext.currentTime);
        this.updateLights();
      }

      const releaseTime = 0.05;
      this.gainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + releaseTime);
      this.woodblockGainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + releaseTime);
    },

    updateOscillatorFrequencies() {
      const clickFrequency = 1000 + (this.bpm - 120) * 10;
      const woodblockFrequency = 1200 + (this.bpm - 120) * 10;
      if (this.clickOscillator) {
        this.clickOscillator.frequency.setValueAtTime(clickFrequency, this.audioContext.currentTime);
      }
      if (this.woodblockOscillator) {
        this.woodblockOscillator.frequency.setValueAtTime(woodblockFrequency, this.audioContext.currentTime);
      }
    },
    updateLights() {
      this.lights = this.lights.map((light, index) =>
        index === 0 ? 'woodblock' : ''
      );
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
      this.updateOscillatorFrequencies();
    },
    decreaseBPM() {
      this.bpm = Math.max(20, this.bpm - 5);
      this.updateOscillatorFrequencies();
    },
    
  },
};
</script>

