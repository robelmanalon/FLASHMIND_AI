<script setup>
import { ref } from 'vue'

defineProps({
	modelValue: { type: String, default: '' },
	placeholder: { type: String, default: '••••••••' },
	autocomplete: { type: String, default: 'current-password' },
	minlength: { type: [Number, String], default: undefined },
})

const emit = defineEmits(['update:modelValue'])
const show = ref(false)
</script>

<template>
	<div class="relative">
		<input
			v-bind="{ placeholder, autocomplete, minlength }"
			:type="show ? 'text' : 'password'"
			:value="modelValue"
			required
			class="mt-2 w-full rounded-xl border border-white/10 bg-white/5 py-3 pl-4 pr-12 text-white outline-none placeholder:text-slate-600 focus:border-cyan-300/60"
			@input="emit('update:modelValue', $event.target.value)"
		/>
		<button
			type="button"
			:aria-label="show ? 'Hide password' : 'Show password'"
			class="absolute right-3 top-1/2 grid h-8 w-8 -translate-y-1/2 place-items-center rounded-lg text-slate-500 transition hover:text-cyan-300"
			@click="show = !show"
		>
			<svg v-if="!show" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
			<svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" /></svg>
		</button>
	</div>
</template>