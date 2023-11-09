# Examples

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at egestas felis. Sed tempor dapibus nibh. Nam convallis purus eu turpis iaculis dictum. Vivamus et purus arcu. Aliquam fringilla, eros ut tempor ultricies, nibh ligula tristique magna, ac venenatis dui lectus eu eros.

## Solve one variable

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at egestas felis. Sed tempor dapibus nibh. Nam convallis purus eu turpis iaculis dictum. Vivamus et purus arcu. Aliquam fringilla, eros ut tempor ultricies, nibh ligula tristique magna, ac venenatis dui lectus eu eros.

1. $\left( 5\pi - 10 \arcsin(x) - 10x \sqrt{1-x^{2}} \right) - 12.4$

| Input          | Value                                                          |
| -------------- | -------------------------------------------------------------- |
| Function       | `( 5 * pi - 10 * asin(x) - 10 * x * sqrt(1 - (x**2)) ) - 12.4` |
| Limit x left   | `-1`                                                           |
| Limit x right: | `1`                                                            |
| Limit y up     | `5`                                                            |
| Limit y down   | `-5`                                                           |
| Iteration      | `30`                                                           |
| Tolerance      | `1e-3`                                                         |
| $x_{0}$        | `-0.76`                                                        |
| $x_{1}$        | `0.99`                                                         |

2. $e^{x} - 2 - \cos(e^{x} - 2)$

| Input         | Value                          |
| ------------- | ------------------------------ |
| Function      | `exp(x) - 2 - cos(exp(x) - 2)` |
| Limit x left  | `-4`                           |
| Limit x right | `2`                            |
| Limit y up    | `2`                            |
| Limit y down  | `-2`                           |
| Iteration     | `30`                           |
| Tolerance     | `1e-3`                         |
| $x_{0}$       | `0.5`                          |
| $x_{1}$       | `2`                            |

## Differential equations

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at egestas felis. Sed tempor dapibus nibh. Nam convallis purus eu turpis iaculis dictum. Vivamus et purus arcu. Aliquam fringilla, eros ut tempor ultricies, nibh ligula tristique magna, ac venenatis dui lectus eu eros.

1. $\textcolor{red}{ \frac{dy}{dx} }= y(x) - x^2 + 1$

| Input     | Value                      |
| --------- | -------------------------- |
| Function  | `y(x).diff(x)=y(x)-x**2+1` |
| Initial X | `0`                        |
| Initial Y | `0.5`                      |
| Steps     | `4`                        |
| Max Value | `2`                        |

2. $\textcolor{red}{ \frac{dy}{dx} } = \frac{x^2 - 1}{y^2}$

| Input     | Value                             |
| --------- | --------------------------------- |
| Function  | `y(x).diff(x)=(x**2-1)/(y(x)**2)` |
| Initial X | `0`                               |
| Initial Y | `2`                               |
| Steps     | `5`                               |
| Max Value | `1`                               |

3. $\textcolor{red}{ \frac{dy}{dx} } = \frac{e^{-x} \sin(2x)}{x} - \frac{1 + x}{x} y(x)$

| Input     | Value                                                     |
| --------- | --------------------------------------------------------- |
| Function  | `diff(y(x)) = ((exp(-x) * sin(2*x))/x) -((1 + x)/x)*y(x)` |
| Initial X | `1`                                                       |
| Initial Y | `2`                                                       |
| Steps     | `10`                                                      |
| Max Value | `3`                                                       |

# how to write function for input _function_

- `asin(x)`
- `exp(x)`
- `ln(x)`
- `log(x)/log(10)` _log base 10_
