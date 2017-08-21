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
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Class Red
 */
public class Red {

    //
    // Fields
    //
    private int   entradas = 0;
    private int   salidas  = 0;
    private int   nCapas;
    private Perceptron[][] capas;
    private Double[][]     sinapsis;
    public  double rata    = 0.01;
    public  double minimo  = 0.001;
    public  int    ciclos  = 10;
    public  int    entrenamientos;
    private ArrayList log;
    private String[] transferencias;

    //
    // Constructors
    //
    public Red (int entradas, int salidas, int[] layers, String[] funciones)
    { 
        nCapas   = layers.length;
        this.entradas = entradas;
        this.salidas  = salidas;
        this.transferencias = funciones;
        this.entrenamientos = 0;
        this.log = new ArrayList();
        int max  = 0;
        byte[] ascii = (new String("A")).getBytes();

        for(int i=0; i<nCapas; i++)
            max = layers[i]>max ?layers[i] :max;

        capas    = new Perceptron[nCapas][max];
        sinapsis = new Double[nCapas+1][max];
        limpiarSinapsis();

        int inputs = entradas;

        for(int i=0; i<nCapas; i++)
        {
            for(int j=0; j<max; j++)
            {
                capas[i][j] = j<layers[i] ?new Perceptron(inputs, funciones[i]) :null;
                if(capas[i][j] != null)
                    capas[i][j].setId(""+((char)(ascii[0]+i))+i+""+j);
            }
            inputs = layers[i];
        }
    }
    
    public Red(String xml)
    {
        
    }

    //
    // Methods
    //
    private void limpiarSinapsis()
    {
        for(int i=0; i<sinapsis.length; i++)
            for(int j=0; j<sinapsis[i].length; j++)
                this.sinapsis[i][j] = null;
    }

    /**
     * simular
     * 
     * @param inputs
     * @return Double[]
     * 
     * Propagacion hacia adelante del la red neuronal, devolviendo una salida
     * en funcion de los argumentos de entrada.
     * 
     * Mas detalle en profundidad visitar:
     * http://galaxy.agh.edu.pl/~vlsi/AI/backp_t_en/backprop.html
     **/
    public Double[] simular(Double[] inputs)
    {
        Double outputs[] = new Double[salidas];
        int i=0, j=0, n=0;

        for(n=0; n<inputs.length && n<sinapsis[0].length; n++)
            sinapsis[0][n] = inputs[n];

        //log.add("\nRed.simular(inputs.lenght:"+inputs.length+")\n");

        try
        {
            for(i=0; i<nCapas; i++)
                for(j=0; j<capas[i].length && j<salidas; j++)
                    if(capas[i][j] != null)
                    {
                        for(n=0; n<sinapsis[i].length && n<capas[i][j].entradas.length && sinapsis[i][n]!=null; n++)
                            capas[i][j].entradas[n] = sinapsis[i][n];

                        sinapsis[i+1][j] = capas[i][j].calcular();

                        if(i == nCapas-1)
                            outputs[j] = capas[i][j].salida;
                    }
        }
        catch(Exception e)
        {
            ArrayList cap = new ArrayList();
            ArrayList sin = new ArrayList();
            ArrayList pes = new ArrayList();

            log.add("Red.simular(inputs.lenght:"+inputs.length+") Exepcion!\n"+
                    "i=[0.."+(capas.length-1)+"], j=[0.."+(capas[0].length-1)+"]\n" +
                    "Punto de ruptura: i="+i+" j="+j+" n="+n);

            for(i=0; i<capas.length; i++)
            {
                ArrayList out = new ArrayList();
                for(j=0; j<capas[i].length && capas[i][j]!=null; j++)
                    out.add(capas[i][j].getEntradas());
                cap.add("Capa Entrada "+i+out.toString()+"\n");
            }
            for(i=0; i<capas.length; i++)
            {
                ArrayList out = new ArrayList();
                for(j=0; j<capas[i].length && capas[i][j]!=null; j++)
                    out.add(capas[i][j].getConfiguracion());
                pes.add("Capa pesos "+i+out.toString()+"\n");
            }
            for(i=0; i<sinapsis.length; i++)
            {
                ArrayList out = new ArrayList();
                for(j=0; j<sinapsis[i].length; j++)
                    out.add(sinapsis[i][j]);
                sin.add("Capa sinapsis "+i+out.toString()+"\n");
            }
            log.add("Estado capas:\n"+cap.toString()+"\n"+
                    "Estado pesos:\n"+pes.toString()+"\n"+
                    "Estado sinapsis:\n"+sin.toString()+"\n" +
                    "ERROR: '"+e.toString()+"'\n");
        }

        return outputs;
    }

    /** 
     * entrenar
     *
     * Estructura y aprendizaje:
     * - Capa de entrada con n neuronas.
     * - Capa de salida con m neuronas.
     * - Al menos una capa oculta de neuronas.
     * - Cada neurona de una capa recibe entradas de todas las
     *   neuronas de la capa anterior y envía su salida a todas
     *   las neuronas de la capa posterior. No hay conexiones
     *   hacia atrás ni laterales entre neuronas de la misma capa.
     *
     * Mas detalle en profundidad visitar:
     * http://galaxy.agh.edu.pl/~vlsi/AI/backp_t_en/backprop.html
     **/
    public Double entrenar(Double[][] inputs, Double[][] outputs)
    {
        Double[][] salidas   = new Double[outputs.length][outputs[0].length],
                   sigma     = new Double[outputs.length][outputs[0].length];
        ArrayList resultados = new ArrayList();

        ciclos = inputs[0].length;
        
        log.add("\nRed.entrenar(inputs:"+inputs.length+"x"+inputs[0].length+"\n"+
                this.array2list(inputs).toString()+
                "\noutputs:"+outputs.length+"x"+outputs[0].length+"\n"+
                this.array2list(outputs).toString()+");\n");
        log.add("salidas:"+salidas.length+"x"+salidas[0].length+"\n"+
                "sigma:"+sigma.length+"x"+sigma[0].length+"\n");

        try
        {
           log.add("\npaso 1:\n");
            // paso 1: Se inicializan los pesos de todas las neuronas con valores
            //         aleatorios rango [0..1]
            for(int i=0; i<nCapas && this.entrenamientos == 0; i++)
                for(int j=0; j<capas[i].length && capas[i][j] != null; j++)
                    capas[i][j].inicializarPesos();

            this.entrenamientos++;

            log.add("\npesos iniciales: \n"+this.getConfiguracion().toString()+"\n");
            log.add("datos=[0.."+inputs[0].length+"]\n");
            int epochs = ciclos;

            do
            {
                for(int datos=0; datos < inputs[0].length; datos++)
                {
                        // paso 2: Seleccionar el siguiente par de entrenamiento del conjunto de
                    //         entrenamiento, aplicando el vector de entrada a la entrada de la red.
                    log.add("\niteracion:"+(epochs--)+", datos["+datos+"]\n");
                    log.add("\npaso 2:\n");
                    Double[] entradas = new Double[this.entradas];

                    for(int i=0; i<this.entradas; i++)
                        entradas[i] = inputs[i][datos];

                    // paso 3: Calcular salida de la red
                    log.add("\npaso 3:\n");
                    Double resultado[] = simular(entradas);

                    for(int i=0; i<resultado.length; i++)
                        salidas[i][datos] = resultado[i];
 
                    double error[]   = new double[outputs.length];
                    boolean underMin = true;

                    // calcula el delta de error de la red buscando un minimo
                    for(int i=0; i<outputs.length; i++)
                    {
                        error[i] = outputs[i][datos] - salidas[i][datos];
                        underMin = Math.abs(error[i]) > minimo && underMin ?false :underMin;
                        log.add("error["+i+"]:"+String.format("%08f",error[i])+" = outputs["+i+"]["+datos+"]:"+String.format("%08f",outputs[i][datos])+" - salidas["+i+"]["+datos+"]:"+String.format("%08f",salidas[i][datos])+"; "+String.format("%08f",error[i])+" < "+minimo+" => "+underMin+"\n");
                    }

                    if(underMin) break;

                    log.add("\npaso 4:\n");
                    // paso 4: Calcular el error entre la salida de la red y la salida deseada
                    //         (vector objetivo de par de entrenamiento)
                    for(int i=nCapas-1; i>=0 && capas[i] != null; i--)
                        for(int j=0; j<capas[i].length && capas[i][j] != null && outputs[i][j] != null && salidas[i][j] != null; j++)
                        {
                            double delta = i == nCapas-1 ?outputs[i][j] - salidas[i][j]: getError(i+1,j);
                            capas[i][j].setSigma(delta);
                        }

                    log.add("\npaso 5:\n");
                    // paso 5: Ajustar los pesos de la red para minimizar este error
                    for(int i=0; i<nCapas && capas[i] != null; i++)
                        for(int j=0; j<capas[i].length && capas[i][j] != null; j++)
                            capas[i][j].backPropagation(capas[i][j].getError(rata)); // * sinapsis[i][j]);

                    log.add("\npaso 6:\n");
                    // paso 6: Repetir de 1 al 4 para cada vector del conjunto de entrenamiento
                    //         hasta que el error del conjunto entero sea aceptablemente bajo
                    String conf = this.getConfiguracion();
                    resultados.add(conf);
                    log.add("\nRESULTADOS:"+conf+"\n");
                }
            }
            while(epochs > 0);
        }
        catch(Exception e)
        {
            System.out.println("EXCEPCION! '"+e.toString()+"'\nDETALLES LOG:\n"+log.toString());
            Logger.getLogger(Red.class.getName()).log(Level.SEVERE, null, e);
        }
        finally
        {
            System.out.println("EXITO!\nDETALLES LOG:\n"+log.toString());
        }

        return null;
    }

    //
    // Accessor methods
    //

    public double getError(int capa, int peso)
    {
        double error = 0.0;

        for(int i=0; i<capas[capa].length && capas[capa][i] != null; i++)
            error += capas[capa][i].getSigma() * capas[capa][i].getPeso(peso);

        return error;
    }

    public int getEntradas() {
        return entradas;
    }

    public void setEntradas(int entradas) {
        this.entradas = entradas;
    }

    public int getNcapas() {
        return nCapas;
    }

    public void setNcapas(int nCapas) {
        this.nCapas = nCapas;
    }

    public int getSalidas() {
        return salidas;
    }

    public void setSalidas(int salidas) {
        this.salidas = salidas;
    }
    
    //
    // Other methods
    //

    public String getConfiguracion()
    {
        StringBuffer net  = new StringBuffer();
        byte[] ascii = (new String("A")).getBytes();

        for(int i=0; i<nCapas; i++)
        {
            Hashtable conf = new Hashtable();
            String capa = ""+((char)(ascii[0]+i));
            conf.put(capa, new ArrayList());
            conf.put("func."+capa, this.transferencias[i]);

            for(int j=0; j<capas[i].length && capas[i][j] != null; j++)
                ((ArrayList)conf.get(capa)).add(capas[i][j].getConfiguracion());
            
            net.append(conf.toString()+"\n");
        }

        return net.toString();
    }

    private ArrayList array2list(Double[][] data)
    {
        ArrayList datos = new ArrayList();
        for(int i=0; i<data.length; i++)
        {
            datos.add(new ArrayList());
            for(int j=0; j<data[i].length; j++)
                ((ArrayList)datos.get(i)).add(String.format("%08f", data[i][j]));
        }
        return datos;
    }
}
