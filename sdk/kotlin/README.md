# Kotlin / Android

Kotlin has first-class compatibility through the JVM implementation in `sdk/java/` and the repository's Android client. Kotlin can construct `world.navis.cosmos.Synapse.State` and `Synapse.Feature` directly without a second copy of the kernel math.

```kotlin
val state = Synapse.State()
val update = state.update(arrayOf(Synapse.Feature(0.5, 0.9), Synapse.Feature(-0.25, 0.8)), 0.85)
println(update.vector().contentToString())
```

For Android sensor acquisition, keep permissions and raw sensor handling on-device, then either use the JVM kernel or post neutral observations to `/v1/observe`.
