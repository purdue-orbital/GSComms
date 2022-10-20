import { writable } from "svelte/store";
import State from "../data/State";

class StateStore {
    public subscribe: Function;
    private _set: Function;
    private _update: Function;

    private _launchState: State = State.NotStarted;
    private _abortState: State = State.NotStarted;
    private _cutState: State = State.NotStarted;

    constructor() {
        let { subscribe, set, update } = writable(this);
        this.subscribe = subscribe;
        this._set = set;
        this._update = update;
    }

    async launch() {
        this._update((that: StateStore) => {
            that._launchState = State.Processing;
            return that;
        });
    }

    async abort() {

    }

    async cut() {
        
    }

    async update() {
        
    }

    
    public get launchState() : State {
        return this._launchState;
    }

    
    public get abortState() : State {
        return this._abortState;
    }

    
    public get cutState() : State {
        return this._cutState;
    }
    
    
    
}

const stateStore = new StateStore();

export { stateStore, type StateStore }