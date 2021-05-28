<template>
    <div v-if="currentTask == n">
        <div>
            {{ text }} <span class="bigger">{{ task }}</span> ?<br>
            <span class="smaller">Ответ введите в той же системе счисления, без лишних разделителей</span>
        </div>
        <div class="flex">
            <input type="text" v-model="answer" placeholder="Введите ответ" @keydown="$event.which == 13 && $emit('answer', answer)" ref="ans">
            <input type="button" value="Далее" @click="$emit('answer', answer)">
            <input type="button" :value="showAnswer ? 'Скрыть ответ' : 'Посмотреть ответ'" @click="showAnswer = !showAnswer" v-if="train">
        </div>
        <div v-if="showAnswer" style="margin-top: 8px">
            <div>Правильный ответ: {{ correctAnswer }}</div>
            <div v-if="hint">{{ hint }}</div>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    props: ['task', 'n', 'currentTask', 'train', 'hint', 'correctAnswer', 'text'],
    data: () => ({
        answer: '',
        showAnswer: false,
    }),
    updated() {
        if (this.$refs.ans)
            this.$refs.ans.focus();
    }
}
</script>

<style scoped>
input {
    margin: 0pt;
    margin-left: 10px;
}
input[type="text"] {
    width: 80%;
}
input[type="button"] {
    flex-grow: 1;
}
.flex {
    display: flex;
    margin-top: 8pt;
}
div {
    text-align: left;
}
.smaller {
    font-size: 12px;
}
.bigger {
    font-size: 24px;
}
</style>