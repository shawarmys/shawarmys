class Service {
  getRoot() {
    return { message: "Server is running" };
  }

  getHealth() {
    return { status: "ok" };
  }

  async getMetadata() {
    // TODO: wire up DB query
    return { importedFiles: 0, successfulMappings: 0, mappingAlerts: 0 };
  }

  async getImportedFiles() {
    // TODO: wire up DB query
    return [];
  }

  async getDataSourcesSummary() {
    // TODO: wire up DB query
    return [];
  }

  async getDataGroupsSummary() {
    // TODO: wire up DB query
    return [];
  }

  handleFileUpload(file: Express.Multer.File) {
    return {
      name: file.originalname,
      size: file.size,
      mimetype: file.mimetype,
    };
  }
}

export const service = new Service();
