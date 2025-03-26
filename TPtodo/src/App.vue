<script>
import TodoItem from './components/TodoItem.vue';

let URL_REST = 'http://localhost:5000/todos';

let data = {
    todoID: 2,
    todos: [
        { id: 1, text: 'Faire les courses', checked: true },
        { id: 2, text: 'Apprendre REST', checked: false }
    ],
    title: 'Mes tâches',
    newItem: ''
};

export default {
    data() {
        return data;
    },
    methods: {
      addItem: function () {
            let text = this.newItem.trim();
            if (text) {
                fetch(URL_REST, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json',
                      'Access-Control-Allow-Origin':'*'
                     },
                    body: JSON.stringify({ text: text, checked: false })
                })
                .then(response => response.json())
                .then(data => {
                    this.todos.push(data);
                    this.newItem = '';
                });
            }
        },
        removeItem: function (event) {
            fetch(`${URL_REST}/${event.id}`, { method: 'DELETE' })
            .then(() => {
                this.todos = this.todos.filter(todo => todo.id !== event.id);
            });
        },
        editItem: function (event) {
            fetch(`${URL_REST}/${event.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: event.text })
            })
            .then(response => response.json())
            .then(data => {
                let todo = this.todos.find(todo => todo.id === event.id);
                if (todo) {
                    todo.text = data.text;
                }
            });
        },
        fetchTodos: function () {
            fetch(URL_REST,
            {method: 'GET',
            headers: { 'Content-Type': 'application/json',
                      'Access-Control-Allow-Origin':'*'
                      }})
            .then(response => response.json())
            .then(data => {
                this.todos = data;
            });
        }
    },
    mounted() {
        this.fetchTodos();
    },
    components: { TodoItem }
}
</script>

<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
  <div class="container">
      <h2>{{ title }}</h2>
      <ol>
          <TodoItem v-for="todo in todos" :key="todo.id" :todo="todo" @remove="removeItem" @edit="editItem"></TodoItem>
      </ol>
      <div class="input-group">
          <input v-model="newItem" @keyup.enter="addItem" placeholder="Ajouter une tâche à la liste" type="text" class="form-control">
          <span class="input-group-btn">
              <button @click="addItem" class="btn btn-default" type="button">Ajouter</button>
          </span>
      </div>
  </div>
</template>