<script lang="ts">
    import { onDestroy, onMount } from 'svelte';
    import StateWidgetType from './data/StateWidgetType';
    import StateWidget from './StateWidget.svelte';
    import {telemetryStore} from './stores/TelemetryStore';

    let interval: NodeJS.Timer;

    onMount(() => interval = setInterval(() => telemetryStore.update(), 30_000));

    onDestroy(() => clearInterval(interval));
</script>

<svelte:head>
	<title>Purdue Orbital Ground Station</title>
	<meta name="robots" content="noindex nofollow" />
	<html lang="en" />
</svelte:head>

<main>
    <h1 style="text-align: center;">GS: Comms</h1>
    <hr>
    <br>
    <br>
    <div class="main-page-container">

        <div class="map">
            Map
            <hr>
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
        
        <StateWidget buttonType={StateWidgetType.LAUNCH}/>
        <StateWidget buttonType={StateWidgetType.ABORT}/>
        <StateWidget buttonType={StateWidgetType.CUT}/>

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
    .navbar {grid-area: navbar-grid;}
    .divider {grid-area: divider;}
    .map {grid-area: map-grid;}
    .statistics {grid-area: statistics-grid;}
    .abort {grid-area: abort-grid;}
    .launch {grid-area: launch-grid;}
    .deflate {grid-area: deflate-grid;}
    .stabilize {grid-area: stabilize-grid;}
    .footer {grid-area: footer-grid;}

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
    }

    :global(.button) {
        border: none;
        color: white;
        display: inline-block;
        font-size: 15px;
        cursor: pointer;
        padding: 5%;
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
</style>