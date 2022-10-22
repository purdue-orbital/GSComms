<script lang="ts">
    import { onDestroy, onMount } from 'svelte';
    import State from './data/State';
    import StateWidgetType from './data/StateWidgetType';
    import Map from './Map.svelte';
    import StateWidget from './StateWidget.svelte';
    import { StateStore, stateStore } from './stores/StateStore';
    import {telemetryStore} from './stores/TelemetryStore';

    let interval: NodeJS.Timer = setInterval(() => telemetryStore.update(), 30_000);
    let timeInterval: NodeJS.Timer;
    let start: any = new Date();
    let time: any = new Date();
    
    $: hours = Math.floor(minutes / 60);
    $: minutes = Math.floor(seconds / 60);
    $: seconds = Math.floor(diff / 1000);
    $: millis = diff % 1000;
    $: diff = time - start;

    let disableLaunch: boolean = false;
    let disableAbort: boolean = true;
    let disableCut: boolean = true;

    const zeroPad = (num, places) => String(num).padStart(places, '0');

    const unsub = stateStore.subscribe((newState: StateStore) => {
        disableLaunch = newState.launchState !== State.NotStarted;
        disableAbort = newState.abortState !== State.NotStarted || newState.launchState !== State.Done;
        disableCut = newState.cutState !== State.NotStarted || disableAbort;

        if (newState.launchState === State.Processing) {
            start = new Date();
            timeInterval = setInterval(() => time = new Date(), 1);
        } else if (newState.abortState === State.Done) {
            clearInterval(timeInterval);
            timeInterval = null;
        }
    });

    onMount(() => stateStore.update());

    onDestroy(() => {
        if (timeInterval) clearInterval(timeInterval);
        clearInterval(interval);
        unsub();
    });
</script>

<main>
    <div class="header">
        <img src="images/OrbitalLogo.png" class="logo" alt="Purdue Orbital Logo">
        <h1>Ground Station</h1>
    </div>

    <div class="main-page-container">

        <div class="map">
            <Map/>
        </div>
        <div class="statistics">
            Telemetry Data
            <hr>
            <div class="stats-numbers">
                <div>Temp (C):</div>
                <div>GPS (x): </div>
                <div>GPS (y): </div>
                <div>GPS (z): </div>
                <div>Acceleration (x): </div>
                <div>Acceleration (y): </div>
                <div>Acceleration (z): </div>
                <div>Angular Velocity: </div>
            </div>
        </div>
        
        <StateWidget buttonType={StateWidgetType.LAUNCH} onClick={() => stateStore.launch()} disabled={disableLaunch}/>
        <StateWidget buttonType={StateWidgetType.ABORT} onClick={() => stateStore.abort()} disabled={disableAbort}/>
        <StateWidget buttonType={StateWidgetType.CUT} onClick={() => stateStore.cut()} disabled={disableCut}/>

        <div class="time">
            <h4>Mission Time</h4>
            <h1 class="time-font">
                {hours}:{zeroPad((minutes % 60).toString(), 2)}:{zeroPad((seconds % 60).toString(), 2)}.{zeroPad(millis.toString(), 3)}
            </h1>
        </div>


    </div>
</main>

<style>
    .time-font {
        font-family: monospace;
    }

    .map {
        grid-area: map-grid;
    }
    .statistics {grid-area: statistics-grid;}
    .time {grid-area: time-grid;}

    .main-page-container {
    display: grid;
    grid-template-areas:
        'map-grid map-grid time-grid time-grid time-grid statistics-grid'
        'map-grid map-grid time-grid time-grid time-grid statistics-grid'
        'map-grid map-grid launch-grid abort-grid cut-grid statistics-grid'
        'map-grid map-grid launch-grid abort-grid cut-grid statistics-grid';
    gap: 25px;
    background-color: white;
    padding: 10px;
    }

    :global(.main-page-container > div) {
        background-color: rgb(229, 226, 226);
        text-align: center;
        padding: 20px;
        font-size: 30px;
        border-radius: 10px;
    }

    :global(.main-page-container > div > h4) {
        margin: 10px 0;
    }

    :global(.button) {
        border: none;
        color: white;
        display: inline-block;
        font-size: 15px;
        cursor: pointer;
        padding: 10px;
        border-radius: 10px;
        transition: all 100ms ease;
    }

    :global(.button:hover:enabled) {
        box-shadow: rgba(0, 0, 0, 0.22) 0px 19px 43px;
        transform: translate3d(0px, -1px, 0px);
    }

    :global(.button:disabled) {
        filter: grayscale(50%);
        cursor: not-allowed;
    }

    /* Statistics Area */
    .stats-numbers > div {
        padding: 1.5%;
        text-align: left;
        font-size: 20px;
    }

    :global(.states-text) {
        font-size: 20px;
        padding-top: 10px;
    }

    .logo {
        width: 40%;
        background-color: black;
        padding: 5px;
        border-radius: 3px;
    }

    .header {
        align-content: center;
        text-align: center;
    }
</style>