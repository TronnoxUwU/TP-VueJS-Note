<script>
export default {
    props: {
        todo: Object
    },
    methods: {
        suppr: function() {
            this.$emit('remove', { id: this.todo.id });
        },
        save: function() {
            this.$emit('edit', { id: this.todo.id, text: this.todo.text });
        }
    },
    emits: ['remove', 'edit']
}
</script>

<template>
    <li :class="{ 'alert alert-success': todo.checked }">
        <div class="checkbox">
            <label>
                <input type="checkbox" v-model="todo.checked">
                <input type="text" v-model="todo.text">
            </label>
        </div>
        <button class="btn btn-primary" @click="save">Enregistrer</button>
        <button class="btn btn-danger" @click="suppr">Supprimer</button>
    </li>
</template>
