'use strict';
module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        sass: {
            dist: {
                files: {
                    'static/css/estilos.css': 'static/css/estilos.scss'
                }
            }
        },
        watch: {
            css: {
                files: 'static/css/*.scss',
                tasks: ['sass','cssmin','beep:2']
            },
            js: {
                files: 'static/js/app.js',
                tasks: ['uglify','beep:2']
            }
        },
        cssmin: {
            target:{
                files:{
                'static/css/estilos.min.css': 'static/css/estilos.css'
                }
            }
        },

        uglify: {
            dist: {
              files: {
                'static/js/app.min.js': 'static/js/app.js'
              }
            }
        }
    });

    //Register modules to user
    grunt.loadNpmTasks('grunt-beep');
    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-uglify');

    //Register tasks
    grunt.registerTask('default', ['watch']);
};