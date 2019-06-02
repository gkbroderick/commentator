# Reference Cheatsheet for Animation Mixins

These mixins can require a lot of arguments, here is a quick list of the mixins and arguments for animations. Please check the commit history for the time of the last update. These outline the basic `@include` usage for SCSS. Sass uses these mixins with a `+mixin-name(arguments)` syntax.


Standard & Specialized Animations (output full animation and keyframe rules)
-------------------

- Opacity (`fadein`, `fadeout`, `fadeto`)
- Translation (`translateX`, `translateY`, etc.)
- Scale (`zoomenter`, `makepop`, `fadezoombump` `zoombump`, etc.)
- Step Animations


General structure is like so:
```scss
@include /**** name of standard animation mixin ****/ (
    animation-duration,         // optional, 300ms default, must include units
    animation-timing-function,  // optional, ease-in-out default
    animation-delay,            // optional, 0 default
    animation-iteration-count   // optional, default no output (once)
)
```

A slightly different syntax is used for custom variants as well as these animation mixins:
- `fadeto`, `translateto`, `translatetoX`, `translatetoY`, `step-animations` (no `-custom` versions[essentially are custom versions])

please check `_specialized-animation-mixins.scss` for the specifics

---

Animation Base
--------------

```scss
@include animation-base(
    $animation-name,              // Make sure to use the same animation-name as the @keyframes rules
    $animation-duration,          // Default 300ms, must include time units
    $animation-timing-function,   // Default no entry (ease-in-out)
    $animation-delay,             // Default 0, otherwise must include time units
    $animation-fill-mode,         // Default Forwards
    $animation-iteration-count    // Default no entry (once)
)
```

---

Keyframes - Single Property
--------------------------

```scss
@include keyframes-base(
    $animation-name,     // Make sure to use the same animation-name as the base animation mixin
    $property,           // CSS property to animate
    $value-init,         // Initial property value (-loop variants also the 100% value)
    $value-end           // End property value (-loop variants will be the value at $midpoint percentage)
    $midpoint            // Default 50%, determines midpoint of animation

)
```

---

Keyframes - Multiple Properties
----------------------------

```scss
@include keyframes-multiprop(
    $animation-name,         // Make sure to use the same animation-name as the base animation mixin
    $property-map-init,      // Map data of the Initial property values (-loop variants also the 100% value)
    $property-map-end,        // Map data of the end property values (-loop variants will be the value at $midpoint percentage)
    $midpoint                 // Default 50%, determines midpoint of animation
)
```

Map Example

```scss
$map-example: (property1: value1, property2: value2, property3: value3)
```


Keyframes - Custom
----------------

```scss
@include keyframes-custom($animation-name){    // Use animation-name from base animation!
    // Keyframes and rules as you would write them in SCSS
}
```

---

Standard Specialized Animation `-custom` variants
-------------------
```scss
@include /**** name of standard animation mixin ****/-custom (
    custom-name,                // the name to be given to the animation and keyframe rules, needs to be distinct from the regular mixin name to avoid conflicts
    transform-value-1,
    transform-value-2,
    transform-value-etc,        // any number of the values for properties to be manipulated, default to the original mixin's values
    animation-duration,         // optional, 300ms default, must include units
    animation-timing-function,  // optional, ease-in-out default
    animation-delay,            // optional, 0 default
    animation-iteration-count   // optional, default no output (once)
)
```
