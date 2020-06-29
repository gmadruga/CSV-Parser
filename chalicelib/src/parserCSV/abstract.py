import glob
import os
import random
import string
import sys
import time
import base64
import hashlib
import boto3
import re
import unicodedata
from io import StringIO
from multiprocessing.pool import ThreadPool
from pathlib import Path
import pandas as pd

import chalicelib.src.parserCSV.api
from chalicelib.src.utils import ParserResult, ParserConfig, TipoDocumento, ParserStatus
from chalicelib.src.loggerConfig import logger
import json


class AbstractPaser:
    def __init__(self, config):
        self.enc = config.getParserConfig()["encoding"]
        self.csvSeparator = config.getParserConfig()["csvSeparator"]
        self.file = Path(config.getParserConfig()["originFilePath"])
        self.config = config.getConfigJson()
        self.outPutCsvFilePath = None
        self.tipoDocumento = self.getTipoDocumento()
        self.final_df = None
        self.result = ParserResult(config, tipoDocumento=self.tipoDocumento.getTipoDocumento())

    def checkDocumento(self):
        pass

    def finalizeDF(self):
        pass

    def getTipoDocumento(self):
        pass

    def parse(self):
        #           CRIA DIRETORIO E ARQUIVO DE SAIDA
        timeStart = time.time()
        self.outPutCsvFilePath = Path(str(self.file.parent) + '\\' + str(self.file.stem))
        self.outPutFileName = Path(str(self.outPutCsvFilePath) + '\\' + str(self.file.stem) + '.csv')
        logger.debug('Iniciando arquivo no diretorio de saida ' + str(self.outPutCsvFilePath))
        try:
            self.parseDocument()
            if not self.outPutCsvFilePath.exists():
                self.outPutCsvFilePath.mkdir()
            self.saveAndGetHash(self.final_df)
            #       SETTANDO O PARSER RESULT
            self.result.setParserHealth(True)
            self.result.setElapsedTime(timeStart)
            self.result.setStatus(ParserStatus.PARSED)
            # -----------------------------------#
            logger.debug('Arquivo parseado com sucesso!!')
            result = self.result.getParserResult()
            return result
        except Exception as e:
            #           ERRO GENERICO
            self.result.setMessage(str(e))
            self.result.setStatus(ParserStatus.ERROR)
            result = self.result.getParserResult()
            return result

    def saveAndGetHash(self, finalDataframe):
        if type(finalDataframe) is str:
            self.outPutFileName.write_text(finalDataframe,self.enc)
        else:
            string = str(finalDataframe)
            finalDataframe.to_csv(self.outPutFileName,index=True, sep=r';')
            self.result.sethHash(self.getHash(string,hash_function='sha256'))

    def getHash(self, buffer, hash_function='sha1'):
        if hash_function == 'sha1':
            h = hashlib.sha1()
        else:
            h = hashlib.sha256()
        h.update(buffer.encode(encoding=self.enc))
        hash_str = base64.b64encode(h.digest()).decode('utf-8')

        return hash_str


class ParserOperador:

    def __init__(self, request):
        self.dp_df = None
        self.rrg_df = None
        self.elg_df = None
        self.cap_df = None
        self.dcm_df = None
        self.codes = None
        self.dates = None
        self.df = None
        self.values = None
        self.request = request
        self.logger = logger

        self.__parse_request()
        self.get_arquivo_s3()


        # Inicializa alguns atributos

        self.arquivosParseados = []
        self.siglaTipoDocumento = 'SIGLA'
        self.hash = ''

        # Atributos utilizados para retorno no JSON de resposta
        # para auxiliar na etapa de identificacao de Prestador/Operadora
        self.ic_operadora = 'NULL'
        self.ic_prestador = 'NULL'
        self.awsIdArquivoOriginal = ''

    def __parse_request(self):
        self.tipoDocumento = self.request["icMetadata"]['tipoDocumento']
        self.usuario = self.request["icMetadata"]['usuario']

        self.bucketArquivoOriginal = self.request['s3']['bucket']
        self.prefixoArquivoOriginal = self.request['s3']['prefix']
        self.arquivoOriginal = self.request['s3']['filename']
        self.versionIdArquivoOriginal = self.request['s3']['version_id']

    def get_arquivo_s3(self) :
        """
            Método utilizado para recuperar o arquivo csv a ser padronizado no S3
            O arquivo recuperado do S3 é retornado como objeto StringIO
            Dessa forma não há escrita em disco o que permite que a geração do dataframe seja mais rápida
        """
        self.logger.debug('Entrou no metodo getArquivoS3')
        try:
            # Recupera o objeto do S3
            s3 = boto3.resource('s3')
            s3.Bucket(self.bucketArquivoOriginal).download_file(self.prefixoArquivoOriginal+self.arquivoOriginal,
                                                                self.arquivoOriginal)
            self.logger.debug('Saindo do metodo getArquivoS3')

            parser_results = chalicelib.src.parserCSV.api.ParserAPI([self.arquivoOriginal]).runAll()



            return parser_results;
        except Exception as e:
            self.logger.error('Erro ao obter arquivo original do S3')
        self.logger.debug('Saindo do metodo getArquivoS3')

    def upload_file(arquivo, bucket, object_name=None):

        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True