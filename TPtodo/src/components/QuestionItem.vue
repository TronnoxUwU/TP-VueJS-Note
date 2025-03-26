<template>
    <div class="question-item">
      <input v-model="question.name" placeholder="Intitulé de la question" class="form-control" />
      <select v-model="question.type" class="form-control">
        <option value="ouverte">Ouverte</option>
        <option value="choix">Choix</option>
      </select>
      <button @click="$emit('remove')" class="btn btn-danger btn-sm">Supprimer</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'QuestionItem',
    props: {
      question: {
        type: Object,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>
  .question-item {
    margin-bottom: 0.5rem;
  }
  </style>
  