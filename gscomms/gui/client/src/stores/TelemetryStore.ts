import {writable} from 'svelte/store';

class Telemetry {
    public subscribe: Function;
    private _set: Function;
    private _update: Function;

    private time: number = 0;
    private temp: number = 0;

    private gpsX: number = 0;
    private gpsY: number = 0;
    private gpsZ: number = 0;

    private accelX: number = 0;
    private accelY: number = 0;
    private accelZ: number = 0;

    private angularVelocity: number = 0;

    constructor() {
        let { subscribe, set, update } = writable(this);
        this.subscribe = subscribe;
        this._set = set;
        this._update = update;
    }

    async update() {

    }
}

export const telemetryStore = new Telemetry()