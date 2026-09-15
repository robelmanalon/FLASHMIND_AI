<script setup>
import ModalDialog from './ModalDialog.vue'

defineProps({ title: String, message: String, confirmLabel: { type: String, default: 'Confirm' } })
defineEmits(['confirm', 'cancel'])
</script>

<template>
  <ModalDialog :title="title" @close="$emit('cancel')"><p class="text-sm leading-6 text-slate-400">{{ message }}</p><div class="mt-6 flex justify-end gap-3"><button class="rounded-xl border border-white/10 px-4 py-2.5 text-sm font-bold text-slate-300" @click="$emit('cancel')">Cancel</button><button class="rounded-xl bg-red-500/90 px-4 py-2.5 text-sm font-bold text-white" @click="$emit('confirm')">{{ confirmLabel }}</button></div></ModalDialog>
</template>