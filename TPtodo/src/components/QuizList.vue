<template>
    <div class="quiz-list-container">
      <ol>
        <li v-for="quiz in quizzes" :key="quiz.uri" class="quiz-item">
          <span>{{ quiz.name }}</span>
          <!-- Émission d'événements pour la suppression et l'ouverture du panneau d'édition -->
          <button @click="$emit('remove', quiz)" class="btn btn-danger btn-sm">Supprimer</button>
          <button @click="openEditPanel(quiz)" class="btn btn-primary btn-sm">Modifier</button>
        </li>
      </ol>
      <!-- Panneau d'édition (s'affiche lors d'un clic sur "Modifier") -->
      <QuizEditPanel 
        v-if="selectedQuiz" 
        :quiz="selectedQuiz" 
        @close="selectedQuiz = null"
        @update="handleUpdate"
      />
    </div>
  </template>
  
  <script>
  import QuizEditPanel from './QuizEditPanel.vue';
  
  export default {
    name: 'QuizList',
    props: {
      quizzes: {
        type: Array,
        required: true
      }
    },
    data() {
      return {
        selectedQuiz: null
      };
    },
    methods: {
      openEditPanel(quiz) {
        // Création d'une copie pour éviter la modification directe dans la liste affichée
        this.selectedQuiz = JSON.parse(JSON.stringify(quiz));
      },
      handleUpdate(updatedQuiz) {
        this.$emit('update', updatedQuiz);
        this.selectedQuiz = null;
      }
    },
    components: { QuizEditPanel }
  };
  </script>
  
  <style scoped>
  .quiz-list-container {
    padding: 1rem;
  }
  .quiz-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }
  </style>
  