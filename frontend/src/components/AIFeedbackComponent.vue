<template>
    <div class="flex flex-col h-full justify-between">
      <div class="text-gray-500 font-bold text-3xl p-8">{{ this.listening ? msg2 : msg }}</div>
      <div class="text-2xl font-bold">
        <button @click="aiListening" :class="{ 'border-white text-white': !listening, 'border-red-500 text-red-500': listening }" class="border-2 m-4 p-4">
          AI assistant
        </button>
      </div>
    </div>
</template>

<script>

export default {
  name: 'AIFeedbackComponent',
  data() {
    return {
      listening : false,
      msg: "If you want to test whether you are playing properly at this BPM, use the AI Assistant. You have to play once what the MIDI covers. There will be a 4 bit count in.",
      msg2: "AI is recording your playing for analysis. If you stop, you will need to play it again from the start.",
    }
  },
  methods: {
    aiListening() {
      this.listening = !this.listening
      if (this.listening) {
        this.emitEvent();
      }
    },
    emitEvent() {
      this.$emit('ailistening');
    }
  }
}
</script>