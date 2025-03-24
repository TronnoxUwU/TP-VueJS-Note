<script>
export default {
    props: {
        todo: Object
    },
    methods: {
        suppr: function() {
            this.$emit('remove', { id: this.todo.id });
        }
    },
    emits: ['remove']
}
</script>

<template>
    <li :class="{ 'alert alert-success': todo.checked }">
        <div class="checkbox">
            <label>
                <input type="checkbox" v-model="todo.checked"> {{ todo.text }}
            </label>
        </div>
        <input type="button" class="btn btn-danger" value="Supprimer" @click="suppr">
    </li>
</template>
