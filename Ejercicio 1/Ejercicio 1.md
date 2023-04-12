# Ejercicio 1

**Nombre**: Javier Kauer

---

## Pregunta 1
Explique por qué el realizar validaciones del input del usuario en el front-end es una facilidad pero no una medida de seguridad. 

**Respuesta**: Es porque la validación que se este haciendo se hace dentro del archivo .html, es decir un archivo que ya se ha descargado, y que no se tiene que volver a actualizad. Esto no es una medidad de seguridad porque el propio usuario puede modificar el archivo .html.

## Pregunta 2
Usted cuenta con el siguiente codigo HTML:
```html
<div>
    <p>Contador: <span id="contador">0</span></p>
    <button type="button" id="btn-resta">-1</button>
    <button type="button" id="btn-suma">+1</button>
</div>
```
Implemente un contador bidireccional utilizando la plantilla disponible mas abajo, solo programe donde se le indica. Se espera que tras apretar un boton, el contador se actualice sin la necesidad de recargar la pagina. **No esta permitido modificar el HTML**.

**Respuesta**:
```js
// se buscan los elementos necesarios
// --> PROGRAME AQUI!<---
let counter = document.getElementById("contador");
let buttonres = document.getElementById("btn-resta");
let buttonsum = document.getElementById("btn-suma");

let n = 0; // contador

const suma = () => {
    // --> PROGRAME AQUI!<---
    n++;
    counter.innerText = n;
};

const resta = () => {
    // --> PROGRAME AQUI!<---
    n--;
    counter.innerText = n;
};
// asignar respectivamente la funciones al evento "click"
// --> PROGRAME AQUI!<---
buttonres.addEventListener("click", resta);
buttonsum.addEventListener("click", suma);
```

## Pregunta 3

Explique brevemente qué es el HTML semántico. ¿Qué ventajas tiene? De dos ejemplos de etiquetas (*tags*) semánticas.

**Respuesta**: El HTML semántico corresponde a una forma de ocupar HTML con etiquetas únicas. La ventaja principal que presenta HTML semántico corresponde a que es más fácil de leer y enteder, ya que la presencia de etiquetas únicas hace que el significado y uso de ellas sean simples. Ciertos ejemplos corresponden a: "nav" y "article".