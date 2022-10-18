<script lang="ts">
    import type StateWidgetType from "./data/StateWidgetType";

    export let buttonType: StateWidgetType;
</script>

<div style="grid-area: {buttonType.gridPosition};">
    <h5>{buttonType.name}</h5>
    <button class="button" on:click style="background-color: {buttonType.backgroundColor};">{buttonType.name}</button>
    <div class="states-text">Deflate State: N/A</div>
</div>