export interface SynapticFeature{baselineDelta:number;quality:number}
export interface SynapticUpdate{vector:number[];revision:number;confidence:number}
export declare const PHASE_STEP:number;
export declare class SynapseState{readonly dimensions:number;readonly leak:number;readonly inputGain:number;vector:Float64Array;revision:number;constructor(dimensions?:number,leak?:number,inputGain?:number);update(features:SynapticFeature[],confidence?:number):SynapticUpdate;}
export declare function synapticStep(previousState:number[],features:SynapticFeature[],leak?:number,inputGain?:number):number[];
