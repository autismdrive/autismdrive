import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { FileSystemFileEntry, UploadEvent } from 'ngx-file-drop';
import { ReplaySubject } from 'rxjs';
import { SDFormField } from '../form-field';
import { zoomTransition } from '../animations';
import { SDFileAttachment } from '../file-attachment';
import { ApiService } from '../../api.service';
import { NgProgress } from 'ngx-progressbar';
import { ParallelHasher } from 'ts-md5/dist/parallel_hasher';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.scss'],
  animations: [zoomTransition()]
})
export class SDFileUploadComponent implements OnInit {
  @Input() field: SDFormField;
  updateFilesSubject = new ReplaySubject<SDFileAttachment[]>();
  displayedColumns: string[] = [
    'name',
    'display_name',
    'type',
    'size',
    'lastModifiedDate',
    'actions'
  ];
  dropZoneHover = false;
  @ViewChild(NgProgress) progress: NgProgress;

  constructor(private api: ApiService) {
  }

  ngOnInit() {
    if (this.field && this.field.attachments && (this.field.attachments.size > 0)) {
      this.updateFileList();
    }

    this.field.formControl.valueChanges.subscribe(() => {
      this.updateFileList();
    });
  }

  dropped($event: UploadEvent) {
    this.dropZoneHover = false;

    $event.files.forEach((droppedFile, i) => {
      if (droppedFile.fileEntry.isFile) {
        const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
        fileEntry.file(newFile => this.addFile(newFile));
      }
    });
  }

  fileOver($event) {
    this.dropZoneHover = true;
  }

  fileLeave($event) {
    this.dropZoneHover = false;
  }

  formatSize(bytes: number, decimalPlaces = 2): string {
    const sizes = ['KB', 'MB', 'GB', 'TB'];
    const factor = Math.pow(10, decimalPlaces);

    for (let i = 0; i < sizes.length; i++) {
      const divisor = Math.pow(10, (3 * (i + 1)));
      const nextDivisor = Math.pow(10, (3 * (i + 2)));

      if (bytes < nextDivisor) {
        return `${Math.round(bytes / divisor * factor) / factor} ${sizes[i]}`;
      }
    }
  }

  formatDate(d: Date | string | number): string {
    const dateObj = (d instanceof Date) ? d : new Date(d);

    return `
      ${dateObj.getFullYear()}/${dateObj.getMonth()}/${dateObj.getDay()}
      ${dateObj.getHours()}:${dateObj.getMinutes()}
    `;
  }

  truncate(s: string, maxLength = 20): string {
    if (s) {
      if (s.length > (maxLength - 3)) {
        return s.slice(0, maxLength) + '...';
      } else {
        return s;
      }
    } else {
      return '';
    }
  }

  fileIcon(file: SDFileAttachment): string {
    const s = file.mime_type || file.type || file.name || file.file_name;
    const nameArray = s.toLowerCase().split((file.mime_type || file.type) ? '/' : '.');

    if (nameArray.length > 0) {
      return `/assets/filetypes/${nameArray[nameArray.length - 1]}.svg`;
    } else {
      return `/assets/filetypes/unknown.svg`;
    }
  }

  addFile(attachment: SDFileAttachment) {
    const hasher = new ParallelHasher('/assets/md5_worker.js');
    hasher.hash(attachment).then(md5 => {
      attachment.md5 = md5;

      // Check for existing attachments
      let old: SDFileAttachment;
      this.field.attachments.forEach((f: SDFileAttachment) => {
        if (f.file_name === attachment.name) {
          old = f;
        }
      });

      if (old) {
        if (old.md5 !== md5) {
          // New version of existing attachment.
          // Copy all existing metadata to the new file.
          const keys = ['id', 'display_name', 'url', 'mime_type', 'resource_id'];
          keys.forEach(key => attachment[key] = old[key]);
          this.field.attachments.set(md5, attachment);
          this.field.attachments.delete(old.md5);
        } else {
          // Same version of existing attachment. Do nothing.
        }
      } else {

        // New attachment.
        this.field.attachments.set(md5, attachment);
      }

      const apiFn = old ? 'updateFileAttachment' : 'addFileAttachment';

      // Upload changes to S3 immediately
      this.api[apiFn](attachment).subscribe(fa => {

        // Save the returned ID for later.
        this.editFileAttachment(fa, { id: fa.id });

        // Only upload the file blob if the bytes have changed.
        const sameBlob = (old && (old.md5 === attachment.md5));
        if (!sameBlob) {
          this.api
            .addFileAttachmentBlob(fa.id, attachment, this.progress)
            .subscribe(f => {
              this.api.getFileAttachment(fa.id, md5).subscribe(updated => {
                this.editFileAttachment(fa, { url: updated.url });
                this.updateFileList();
              });
            });
        }
      });
      this.updateFileList();
    });

  }

  removeFile($event, attachment: SDFileAttachment) {
    $event.preventDefault();
    this.field.attachments.delete(attachment.md5);
    this.api.deleteFileAttachment(attachment).subscribe(_ => this.updateFileList());
  }

  editFileAttachment(attachment: SDFileAttachment, options) {
    const file = this.field.attachments.get(attachment.md5);

    for (const key in options) {
      if (options.hasOwnProperty(key)) {
        file[key] = options[key];
      }
    }

    this.field.attachments.set(attachment.md5, file);
    this.updateFileList();
  }

  updateFileList() {
    this.updateFilesSubject.next(Array.from(this.field.attachments.values()));
  }

  updateDisplayName($event, attachment: SDFileAttachment) {
    this.editFileAttachment(attachment, { display_name: $event.target.value });
  }
}
