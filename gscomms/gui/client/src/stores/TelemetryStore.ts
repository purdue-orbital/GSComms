import {writable} from 'svelte/store';
import Vector from '../data/Vector';

class Telemetry {
    public subscribe: Function;
    private _set: Function;
    private _update: Function;

    private time: number = 0;
    private temp: number = 0;

    private _gps: Vector = new Vector(0, 0, 0);

    private _accel: Vector = new Vector(0, 0, 0);

    private angularVelocity: number = 0;

    constructor() {
        let { subscribe, set, update } = writable(this);
        this.subscribe = subscribe;
        this._set = set;
        this._update = update;
    }

    async update() {
        
    }

    public get gps() : Vector {
        return this._gps;
    }
    
    public get accel() : Vector {
        return this._accel;
    }
    
}

export const telemetryStore = new Telemetry();