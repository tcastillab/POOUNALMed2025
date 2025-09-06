/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package actividad1_ejercicio12;

/**
 *
 * @author Asus
 */
public class cal_rete {
    static double cal_sal_bruto(double horas,double valorhora){
        double sal_bruto = horas*valorhora;
        return sal_bruto;
    }
        static double cal_por_retencion(double retencion){
        double por_reten= retencion/100;
        return por_reten;
    }
    static double cal_retencion(double por_reten,double sal_bruto){
        double valor_reten= por_reten*sal_bruto;
        return valor_reten;
    }
    static double salario_neto(double sal_bruto,double valor_reten){
        double salario_neto=sal_bruto- valor_reten;
        return salario_neto;
    }
}
