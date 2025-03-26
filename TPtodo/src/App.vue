<script>
import QuizList from './components/QuizList.vue';

const URL_REST = 'http://localhost:5000/todo/api/v1.0/quiz';

export default {
  name: 'App',
  components: { QuizList },
  data() {
    return {
      quizzes: [],
      title: 'Mes Quiz',
      newQuizName: ''
    };
  },
  methods: {
    addQuiz() {
      const name = this.newQuizName.trim();
      if (name) {
        fetch(URL_REST, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: name })
        })
          .then(response => response.json())
          .then(data => {
            this.quizzes.push(data.quiz);
            this.newQuizName = '';
          });
      }
    },
    removeQuiz(quiz) {
      fetch(quiz.uri, { method: 'DELETE' })
        .then(response => {
          if (!response.ok) {
            throw new Error("Erreur lors de la suppression");
          }
          this.quizzes = this.quizzes.filter(q => q.uri !== quiz.uri);
        })
        .catch(error => {
          console.error("Erreur:", error);
        });
    },
    updateQuiz(quiz) {
      fetch(quiz.uri, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: quiz.name, questions: quiz.questions })
      })
        .then(response => response.json())
        .then(data => {
          const index = this.quizzes.findIndex(q => q.uri === quiz.uri);
          if (index !== -1) {
            this.quizzes.splice(index, 1, data.quiz);
          }
        });
    },
    fetchQuizzes() {
      fetch(URL_REST, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      })
        .then(response => response.json())
        .then(data => {
          this.quizzes = data.quiz; // Adaptez selon la structure de votre réponse
        });
    }
  },
  mounted() {
    this.fetchQuizzes();
  }
};
</script>

<template>
  <div class="container">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <h2>{{ title }}</h2>
    <!-- Zone d'ajout d'un quiz -->
    <div class="input-group mb-3">
      <input v-model="newQuizName" @keyup.enter="addQuiz" placeholder="Ajouter un quiz" type="text" class="form-control">
      <button @click="addQuiz" class="btn btn-primary">Ajouter</button>
    </div>
    <!-- Composant de gestion de la liste des quiz -->
    <QuizList 
      :quizzes="quizzes" 
      @remove="removeQuiz" 
      @update="updateQuiz" 
    />
  </div>
</template>
