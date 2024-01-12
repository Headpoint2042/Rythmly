<template>
    <div class="z-10 top-0 left-0 absolute h-screen w-screen flex items-center justify-center">
        <div class="bg-slate-900 p-5 border-4 border-gray-300 rounded-lg h-1/3 w-1/3 flex flex-col">
            <div class="flex justify-end">
                <button @click="triggerClose" class="bg-red-500 size-12 font-black text-white">X</button>
            </div>
            <div class="text-white text-3xl p-5 flex justify-center flex-grow items-center">
                {{ message }}
            </div>
            <div class="flex justify-center" v-if="feedback">
                <button @click="triggerFeedback" class="border-2 p-2 text-2xl font-bold text-green-500 border-green-500">
                    Accept advice
                </button>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        message: String,
        feedback: Boolean,
    },
    methods: {
        triggerClose() {
            this.$emit('close');
        },
        triggerFeedback() {
            this.$emit('feedback');
        }
    }
}
</script>
