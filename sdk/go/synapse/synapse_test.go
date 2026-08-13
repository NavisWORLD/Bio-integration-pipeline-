package synapse
import("math";"testing")
func TestGoldenVector(t *testing.T){ golden:=[]float64{0.02891876766114646,-0.02220725520372799,0.04791912723131752,-0.01459072664788153,0.0025653072604511205,0.012620779875725187,-0.046233655674311015,0.0228828972723213,-0.032941984868177496,0.002413860648239461,0.024589940949515134,-0.02129692995842166}; state:=New12D(); update,err:=state.Update([]Feature{{0.5,0.9},{-0.25,0.8}},0.85); if err!=nil{t.Fatal(err)}; for i:=range golden{if math.Abs(update.Vector[i]-golden[i])>=1e-12{t.Fatalf("index %d mismatch",i)}} }
