/*-----------------------------------------------------------------------*\
 | IMAGESTION                                                            |
 |                                                                       |
 | Copyright (C) 2010-Today, GNUCHILE.CL       - Santiago de Chile       |
 | Licensed under the GNU GPL                                            |
 |                                                                       |
 | Redistribution and use in source and binary forms, with or without    |
 | modification, are permitted provided that the following conditions    |
 | are met:                                                              |
 |                                                                       |
 | o Redistributions of source code must retain the above copyright      |
 |   notice, this list of conditions and the following disclaimer.       |
 | o Redistributions in binary form must reproduce the above copyright   |
 |   notice, this list of conditions and the following disclaimer in the |
 |   documentation and/or other materials provided with the distribution.|
 | o The names of the authors may not be used to endorse or promote      |
 |   products derived from this software without specific prior written  |
 |   permission.                                                         |
 |                                                                       |
 | THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS   |
 | "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT     |
 | LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR |
 | A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT  |
 | OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, |
 | SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT      |
 | LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, |
 | DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY |
 | THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT   |
 | (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE |
 | OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  |
 |                                                                       |
 *-----------------------------------------------------------------------*
 | Author: Miguel Vargas Welch <miguelote@gmail.com>                     |
\*-----------------------------------------------------------------------*/


import java.util.ArrayList;
import java.util.Hashtable;


/**
 * Class Perceptron
 */
public class Perceptron
{

    //
    // Fields
    //
    public  Double[]   entradas;
    private Double[]   pesos;
    public  Double     bias;
    private Double     wBias;
    public  double     salida;
    public  double     sigma;
    private Activacion fnTransf;
    private String     id;

    //
    // Constructors
    //
    public Perceptron (int inputs, String funcion)
    {
        entradas = new Double[inputs];
        pesos    = new Double[inputs];
        bias     = 0d;
        wBias    = 0d;
        salida   = 0d;
        sigma    = 0d;
        fnTransf = new Activacion(funcion);

        for(int i=0; i<inputs; i++)
            entradas[i] = pesos[i] = 0.0;

    }
  
    //
    // Methods
    //
    public Double calcular()
    {
        Double suma = 0.0;
        int i=0;

        try
        {
            for(i=0; i < entradas.length; i++)
                suma += entradas[i] * pesos[i];

            salida = suma + bias*wBias;
        }
        catch(Exception e)
        {
            System.out.println("Perceptron.calcular()\nExepcion!: iteracion i:"+i+" de "+entradas.length+"\n"+e.toString()+"\n");
        }

        return fnTransf.exec(salida);
    }

    /** backPropagation
     *
     * Algoritmo de retropropagación
     *
     * El procedimiento de retropropagación es una forma relativamente eficiente
     * de calcular qué tanto se mejora el desempeño con los cambios individuales
     * en los pesos. Se conoce como procedimiento de retropropagación porque,
     * primero calcula cambios en la capa final, reutiliza gran parte de los
     * mismos cálculos para calcular los cambios de los pesos de la penúltima
     * capa y, finalmente, regresa a la capa inicial.
     *
     */

    public Double backPropagation(double Sigma)  // valor Sigma debe provenir del controlador del ciclo principal
    {
        // ver la forma de ir registrando los valores de los pesos y salidas de cada iteracion
        double avgDelta = 0.0;
        int i = 0;

        try
        {
            for(i = 0; i<pesos.length && pesos[i] != null; i++)
            {
                double delta = Sigma * entradas[i]; // averiguar:  calcular por salida o entrada?
                pesos[i] += delta;
                avgDelta += delta;
            }
        }
        catch(Exception e)
        {
            System.out.println("Perceptron.backPropagation()\nExepcion!: iteracion i:"+i+" de "+pesos.length+"\n"+e.toString()+"\n");
        }

        return avgDelta/pesos.length;  // evaluar si debe retornar valor
    }
    //
    // Accessor methods
    //

    /** setSigma
     *
     * Al comparar la señal de salida con una respuesta deseada o salida objetivo,
     * d(t), se produce una señal de error, e(t), energía de error. Señal de error
     * en la neurona de salida j en la iteración t
     *         e(t)=d(t) - y(t)
     * donde t denota el tiempo discreto, y(t) representa la salida de la capa previa.
     *
     * Regla Delta Generalizada Es una extensión de la regla delta propuesta por Widrow (1960).
     * Se usa en redes con capas intermedias con conexiones hacia delante y cuyas células
     * tienen funciones de activación continuas. Estas funciones continuas son no decrecientes
     * y derivables (la función sigmoidal pertenece a este tipo de funciones).
     *
     */

    public void setSigma(double sigma) {
        this.sigma = sigma;
    }

    public double getSigma() {
        return sigma;
    }

    public double getError(double rata)   // usado en regla de aprendizaje
    {
        // error = objetivo - salida;
        return sigma * fnTransf.train(salida) * rata;
    }

    public Double getBias() {
        return bias;
    }

    public void setBias(Double bias) {
        this.bias = bias;
    }

    public Double getSalida() {
        return salida;
    }

    public void setSalida(Double salida) {
        this.salida = salida;
    }

    public Double getwBias() {
        return wBias;
    }

    public void setwBias(Double wBias) {
        this.wBias = wBias;
    }

    public void setPeso(int idx, Double valor)
    {
        this.pesos[idx] = valor;
    }

    public Double getPeso(int idx)
    {
        return this.pesos[idx];
    }

    public void setId(String valor)
    {
        this.id = valor;
    }

    public String getId()
    {
        return this.id;
    }

    //
    // Other methods
    //

    public void inicializarPesos()
    {
        for(int i=0; i<pesos.length && pesos[i] != null; i++)
            pesos[i] = Math.random();
    }

    public Hashtable getConfiguracion()
    {
        Hashtable conf = new Hashtable();
        conf.put(id, new ArrayList());

        for(int i=0; i<pesos.length; i++)
            ((ArrayList) conf.get(id)).add(String.format("%08f", pesos[i]));

        return conf;
    }

    public Hashtable getEntradas()
    {
        Hashtable conf = new Hashtable();
        conf.put(id, new ArrayList());

        for(int i=0; i<entradas.length; i++)
            ((ArrayList) conf.get(id)).add(entradas[i]);

        return conf;
    }

    public void setConfiguracion()
    {

    }
}
