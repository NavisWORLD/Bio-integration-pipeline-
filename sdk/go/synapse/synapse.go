package synapse

import (
    "errors"
    "math"
)

const PhaseStep = 0.61803398875

type Feature struct { BaselineDelta float64; Quality float64 }
type Update struct { Vector []float64; Revision uint64; Confidence float64 }
type State struct { dimensions int; leak float64; inputGain float64; vector []float64; revision uint64 }

func New(dimensions int, leak, inputGain float64) (*State, error) {
    if dimensions <= 0 { return nil, errors.New("dimensions must be positive") }
    if math.IsNaN(leak) || math.IsInf(leak,0) || leak < 0 || leak >= 1 { return nil, errors.New("leak must be in [0,1)") }
    if math.IsNaN(inputGain) || math.IsInf(inputGain,0) || inputGain < 0 { return nil, errors.New("inputGain must be non-negative") }
    return &State{dimensions:dimensions, leak:leak, inputGain:inputGain, vector:make([]float64,dimensions)}, nil
}

func New12D() *State { state,_ := New(12,0.88,0.12); return state }

func (s *State) Update(features []Feature, confidence float64) (Update,error) {
    if math.IsNaN(confidence) || math.IsInf(confidence,0) || confidence < 0 || confidence > 1 { return Update{},errors.New("confidence must be in [0,1]") }
    for _,f := range features { if math.IsNaN(f.BaselineDelta) || math.IsInf(f.BaselineDelta,0) || math.IsNaN(f.Quality) || math.IsInf(f.Quality,0) || f.Quality < 0 || f.Quality > 1 { return Update{},errors.New("invalid feature") } }
    s.revision++
    if len(features)==0 { return Update{Vector:append([]float64(nil),s.vector...),Revision:s.revision,Confidence:0},nil }
    inputs:=make([]float64,len(features)); for i,f:=range features { inputs[i]=math.Tanh(f.BaselineDelta)*f.Quality }
    next:=make([]float64,s.dimensions); for i:=range next { source:=inputs[i%len(inputs)]; phase:=math.Sin(float64(i+1)*PhaseStep); value:=s.leak*s.vector[i]+s.inputGain*source*phase; next[i]=math.Max(-1,math.Min(1,value)) }
    s.vector=next; return Update{Vector:append([]float64(nil),next...),Revision:s.revision,Confidence:confidence},nil
}
