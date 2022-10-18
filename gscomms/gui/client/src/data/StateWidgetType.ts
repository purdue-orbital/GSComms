export default class StateWidgetType {
    static readonly LAUNCH = new StateWidgetType("Launch", "launch-grid", "green");
    static readonly ABORT = new StateWidgetType("Abort", "abort-grid", "red");
    static readonly CUT = new StateWidgetType("Cut", "cut-grid", "blue");

    public readonly name: string;
    public readonly gridPosition: string;
    public readonly backgroundColor: string;

    constructor(name: string, gridPosition: string, backgroundColor: string) {
        this.name = name;
        this.gridPosition = gridPosition;
        this.backgroundColor = backgroundColor;
    }
}