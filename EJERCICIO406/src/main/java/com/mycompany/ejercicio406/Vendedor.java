/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.ejercicio406;

/**
 *
 * @author Tomas Castilla Barrero
 */
public class Vendedor {
    // ATRIBUTOS
    private String nombre;
    private String apellidos;
    private int edad;

    // CONSTRUCTOR (modificado para incluir la edad si es necesario, 
    // pero mantendremos el tuyo para la lógica de verificarEdad)
    public Vendedor(String nombre, String apellidos) {
        this.nombre = nombre;
        this.apellidos = apellidos;
        this.edad = 0; // Inicializamos a 0
    }

    // GETTERS y SETTERS (recomendado en clases POJO)
    public String getNombre() { return nombre; }
    public String getApellidos() { return apellidos; }
    public int getEdad() { return edad; }

    /**
     * Método que verifica que la edad de un vendedor es apropiada.
     * @throws IllegalArgumentException Excepción de argumento ilegal
     */
    public void verificarEdad(int edad) throws IllegalArgumentException {
        // La lógica debe ser más clara:
        if (edad < 0 || edad > 120) { 
            throw new IllegalArgumentException("La edad no puede ser negativa ni mayor a 120.");
        }
        if (edad < 18) { 
            throw new IllegalArgumentException("El vendedor debe ser mayor de 18 años.");
        }
        
        // Si no se lanza ninguna excepción, la edad es válida
        this.edad = edad; 
    }

    /**
     * Método que devuelve la información como un String para mostrar en la GUI
     */
    @Override
    public String toString() {
        return "<html>**Datos Correctos**<br/>Nombre: " + nombre + 
               "<br/>Apellidos: " + apellidos + 
               "<br/>Edad: " + edad + "</html>";
    }
}


