<script lang="ts">
    import { onDestroy, onMount } from 'svelte';
    import State from './data/State';
    import StateWidgetType from './data/StateWidgetType';
    import Map from './Map.svelte';
    import StateWidget from './StateWidget.svelte';
    import { StateStore, stateStore } from './stores/StateStore';
    import {telemetryStore} from './stores/TelemetryStore';

    let interval: NodeJS.Timer = setInterval(() => telemetryStore.update(), 30_000);

    let disableLaunch: boolean = false;
    let disableAbort: boolean = true;
    let disableCut: boolean = true;

    const unsub = stateStore.subscribe((newState: StateStore) => {
        disableLaunch = newState.launchState !== State.NotStarted;
        disableAbort = newState.abortState !== State.NotStarted || newState.launchState !== State.Done;
        disableCut = newState.cutState !== State.NotStarted || disableAbort;
    });

    onMount(() => stateStore.update());

    onDestroy(() => {
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
            Map
            <hr>
            <Map/>
            <div class="map-bottom">
                <table class="map-table" style="width: 100%;">
                    <tr>
                        <th>Time (s)</th>
                        <th>GPS (x)</th>
                        <th>GPS (y)</th>
                        <th>GPS (z)</th>
                    </tr>
                    <tr>
                        <td>seconds</td>
                        <td>x</td>
                        <td>y</td>
                        <td>z</td>
                    </tr>
                </table>
            </div>

        </div>
        <div class="statistics">
            Telemetry Data
            <hr>
            <div class="stats-numbers">
                <div>Time (s): </div>
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

        <!-- <div class="launch">
            <h5>Launch</h5>
            <button class="button" style="background-color: green;">LAUNCH</button>
            <div class="states-text">Launch State: N/A</div>
        </div>
        <div class="abort">
            <h5>Abort</h5>
            <button class="button" style="background-color: red;">ABORT</button>
            <div class="states-text">Abort State: N/A</div>
        </div>
        <div class="deflate">
            <h5>Deflate/Cut</h5>
            <button class="button" style="background-color: blue;">DEFLATE/CUT</button>
            <div class="states-text">Deflate State: N/A</div>
        </div> -->
        <div class="stabilize">
            <h5>Stabilize</h5>
            <button class="button" style="background-color: blue;">STABILIZE</button>
        </div>


    </div>
</main>

<style>
    .map {
        grid-area: map-grid;
    }
    .statistics {grid-area: statistics-grid;}
    .stabilize {grid-area: stabilize-grid;}

    .main-page-container {
    display: grid;
    grid-template-areas:
        'map-grid map-grid launch-grid abort-grid statistics-grid'
        'map-grid map-grid launch-grid abort-grid statistics-grid'
        'map-grid map-grid cut-grid stabilize-grid statistics-grid'
        'map-grid map-grid cut-grid stabilize-grid statistics-grid';
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

    .map-bottom {
        text-align: bottom;
        font-size: 15px;
        padding-top: 250px;
    }

    table, th, td {
        border: 1px solid black;
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
    }

    .header {
        align-content: center;
        text-align: center;
    }
</style>