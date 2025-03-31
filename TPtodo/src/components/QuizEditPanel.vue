<template>
    <div class="edit-panel">
      <h3>Modifier le Quiz</h3>
      <div class="form-group">
        <label for="quizName">Nom du quiz</label>
        <input id="quizName" v-model="localQuiz.name" type="text" class="form-control" />
      </div>
      <div class="questions-section">
        <h4>Questions</h4>
        <ul>
          <li v-for="(question, index) in localQuiz.questions" :key="question.id || index">
            <input v-model="question.title" placeholder="Intitulé de la question" class="form-control" />
            <select v-model="question.type" class="form-control">
              <option value="ouverte">Ouverte</option>
              <option value="choix">Choix</option>
            </select>
            <button @click="removeQuestion(index)" class="btn btn-danger btn-sm">Supprimer</button>
          </li>
        </ul>
        <button @click="addQuestion" class="btn btn-secondary btn-sm">Ajouter une question</button>
      </div>
      <div class="actions">
        <button @click="submitUpdate" class="btn btn-success">Mettre à jour</button>
        <button @click="$emit('close')" class="btn btn-secondary">Annuler</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'QuizEditPanel',
    props: {
      quiz: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        // Copie locale pour éviter de modifier directement la prop
        localQuiz: JSON.parse(JSON.stringify(this.quiz))
      };
    },
    methods: {
      addQuestion() {
        this.localQuiz.questions.push({
          type: 'ouverte'
        });
      },
      removeQuestion(index) {
        this.localQuiz.questions.splice(index, 1);
      },
      submitUpdate() {
        fetch(this.localQuiz.uri, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: this.localQuiz.name, questions: this.localQuiz.questions })
        })
          .then(response => response.json())
          .then(data => {
            // L'API renvoie le quiz mis à jour sous data.quiz
            this.$emit('update', data.quiz);
            $emit('close');
          })
          .catch(error => console.error("Erreur de mise à jour :", error));
      }
    }
  };
  </script>
  
  <style scoped>
  .edit-panel {
    position: fixed;
    right: 0;
    top: 0;
    width: 300px;
    height: 100%;
    background: #f8f9fa;
    border-left: 1px solid #ddd;
    padding: 1rem;
    overflow-y: auto;
    box-shadow: -2px 0 5px rgba(0,0,0,0.1);
  }
  .form-group,
  .questions-section,
  .actions {
    margin-bottom: 1rem;
  }
  </style>
  