<script lang="ts">
    import StateWidgetType from './data/StateWidgetType';
    import { bind } from 'svelte-simple-modal';
    import ConfirmModal from './ConfirmModal.svelte';
    import {modal} from './stores/ModalStore'
    import State from './data/State';
    import { stateStore } from './stores/StateStore';
    import { onDestroy } from 'svelte';

    export let buttonType: StateWidgetType;
    export let onClick: Function;
    export let disabled: boolean = false;

    let state: State = State.NotStarted;

    const unsub = stateStore.subscribe(newState => {
        if (buttonType === StateWidgetType.LAUNCH) {
            state = newState.launchState;
        } else if (buttonType === StateWidgetType.ABORT) {
            state = newState.abortState;
        } else {
            state = newState.cutState;
        }
    });

    onDestroy(unsub);

    const showModal = () => modal.set(bind(ConfirmModal, { 
        title: `Are you sure you want to ${buttonType.name.toLowerCase()}?`,
        body: 'This action is irreversible!',
        onConfirm: onClick
    }));
</script>

<div style="grid-area: {buttonType.gridPosition};">
    <h5>{buttonType.name}</h5>
    <button class="button" on:click={showModal} disabled={disabled} style="background-color: {buttonType.backgroundColor};">{buttonType.name.toUpperCase()}</button>
    <div class="states-text"><strong>{buttonType.name} State:</strong><br/>{state}</div>
</div>